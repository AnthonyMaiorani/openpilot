import numpy as np
from openpilot.selfdrive.controls.lib.drive_helpers import CONTROL_N, MIN_SPEED, get_speed_error
from openpilot.selfdrive.controls.lib.desire_helper import DesireHelper
import cereal.messaging as messaging
from cereal import log
from openpilot.common.params import Params
from openpilot.selfdrive.controls.lib.road_edge_detector import RoadEdgeDetector
from openpilot.common.conversions import Conversions as CV
from openpilot.selfdrive.controls.lib.lateral_mpc_lane_planner import LateralMpcLanePlanner

TRAJECTORY_SIZE = 33
CAMERA_OFFSET = 0.04

class LateralPlanner:
  def __init__(self, CP, debug=False):
    self.DH = DesireHelper()
    self.params = Params()
    self.param_read_counter = 0

    # for road edge dection
    self.RED = RoadEdgeDetector()
    self.RED.set_enabled(self.params.get_bool("dp_lateral_road_edge_detection"))

    # for lane priority mode
    self.LMLP = LateralMpcLanePlanner(CP, TRAJECTORY_SIZE, debug)
    self.LMLP.set_enabled(self.params.get_bool("dp_lat_lane_priority_mode"))
    self.LMLP.set_speed(int(self.params.get("dp_lat_lane_priority_mode_speed_based", encoding="utf-8")) * CV.KPH_TO_MS)
    self._dp_lat_lane_priority_mode_active = False

    # for lane change assist speed
    self._dp_lat_lane_change_assist_speed = int(self.params.get("dp_lat_lane_change_assist_speed", encoding="utf-8")) * CV.KPH_TO_MS

    # Vehicle model parameters used to calculate lateral movement of car
    self.factor1 = CP.wheelbase - CP.centerToFront
    self.factor2 = (CP.centerToFront * CP.mass) / (CP.wheelbase * CP.tireStiffnessRear)
    self.last_cloudlog_t = 0
    self.solution_invalid_cnt = 0

    self.path_xyz = np.zeros((TRAJECTORY_SIZE, 3))
    self.velocity_xyz = np.zeros((TRAJECTORY_SIZE, 3))
    self.v_plan = np.zeros((TRAJECTORY_SIZE,))
    self.x_sol = np.zeros((TRAJECTORY_SIZE, 4), dtype=np.float32)
    self.v_ego = MIN_SPEED
    self.l_lane_change_prob = 0.0
    self.r_lane_change_prob = 0.0

    self.debug_mode = debug

  def update(self, sm):
    v_ego_car = sm['carState'].vEgo

    # Parse model predictions
    md = sm['modelV2']
    if len(md.position.x) == TRAJECTORY_SIZE and len(md.velocity.x) == TRAJECTORY_SIZE and len(md.lateralPlannerSolution.x) == TRAJECTORY_SIZE:
      self.path_xyz = np.column_stack([md.position.x, md.position.y, md.position.z])
      self.velocity_xyz = np.column_stack([md.velocity.x, md.velocity.y, md.velocity.z])
      car_speed = np.linalg.norm(self.velocity_xyz, axis=1) - get_speed_error(md, v_ego_car)
      self.v_plan = np.clip(car_speed, MIN_SPEED, np.inf)
      self.v_ego = self.v_plan[0]
      self.x_sol = np.column_stack([md.lateralPlannerSolution.x, md.lateralPlannerSolution.y, md.lateralPlannerSolution.yaw, md.lateralPlannerSolution.yawRate])

    # Lane change logic
    desire_state = md.meta.desireState
    if len(desire_state):
      self.l_lane_change_prob = desire_state[log.LateralPlan.Desire.laneChangeLeft]
      self.r_lane_change_prob = desire_state[log.LateralPlan.Desire.laneChangeRight]
    lane_change_prob = self.l_lane_change_prob + self.r_lane_change_prob

    edge_detected_left, edge_detected_right = self.RED.get_road_edge_detected(md.roadEdgeStds, md.laneLineProbs, sm['carState'].leftBlinker, sm['carState'].rightBlinker)
    self.DH.update(sm['carState'], sm['carControl'].latActive, lane_change_prob, edge_detected_left, edge_detected_right, self._dp_lat_lane_change_assist_speed)

    # only allow lane priority mode when not changing lanes
    self._dp_lat_lane_priority_mode_active = False
    if self.LMLP.is_enabled() and not sm['carState'].leftBlinker and not sm['carState'].rightBlinker:
      self.LMLP.set_lane_line_probs(md.laneLineProbs)
      if self.LMLP.should_activate():
        self.LMLP.parse_model(md, v_ego_car)
        self._dp_lat_lane_priority_mode_active = True
        self.path_xyz, self.x_sol = self.LMLP.update(sm['controlsState'].curvature)

  def publish(self, sm, pm):
    plan_send = messaging.new_message('lateralPlan')
    plan_send.valid = sm.all_checks(service_list=['carState', 'controlsState', 'modelV2'])

    lateralPlan = plan_send.lateralPlan
    lateralPlan.modelMonoTime = sm.logMonoTime['modelV2']
    lateralPlan.dPathPoints = self.path_xyz[:,1].tolist()
    lateralPlan.psis = self.x_sol[0:CONTROL_N, 2].tolist()

    lateralPlan.curvatures = (self.x_sol[0:CONTROL_N, 3]/self.v_ego).tolist()
    lateralPlan.curvatureRates = [float(0) for _ in range(CONTROL_N-1)] # TODO: unused

    lateralPlan.mpcSolutionValid = bool(1)
    lateralPlan.solverExecutionTime = 0.0
    if self.debug_mode:
      lateralPlan.solverState = log.LateralPlan.SolverState.new_message()
      lateralPlan.solverState.x = self.x_sol.tolist()

    lateralPlan.desire = self.DH.desire
    lateralPlan.useLaneLines = self._dp_lat_lane_priority_mode_active
    lateralPlan.laneChangeState = self.DH.lane_change_state
    lateralPlan.laneChangeDirection = self.DH.lane_change_direction

    pm.send('lateralPlan', plan_send)

    # dp - extension
    plan_ext_send = messaging.new_message('lateralPlanExt')

    plan_ext_send.valid = True

    lateralPlanExt = plan_ext_send.lateralPlanExt
    # needed for VTC
    lateralPlanExt.dPathWLinesX = [float(x) for x in self.path_xyz[:, 0]]
    lateralPlanExt.dPathWLinesY = [float(y) for y in self.path_xyz[:, 1]]

    pm.send('lateralPlanExt', plan_ext_send)
