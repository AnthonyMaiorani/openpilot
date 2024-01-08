#pragma once
#include "rednose/helpers/ekf.h"
extern "C" {
void car_update_25(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void car_update_24(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void car_update_30(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void car_update_26(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void car_update_27(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void car_update_29(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void car_update_28(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void car_update_31(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void car_err_fun(double *nom_x, double *delta_x, double *out_7890812005855138291);
void car_inv_err_fun(double *nom_x, double *true_x, double *out_1799861052992404131);
void car_H_mod_fun(double *state, double *out_3019605320337164716);
void car_f_fun(double *state, double dt, double *out_5784340983378173671);
void car_F_fun(double *state, double dt, double *out_3386400791859586202);
void car_h_25(double *state, double *unused, double *out_7212104341795181307);
void car_H_25(double *state, double *unused, double *out_7155521575935903180);
void car_h_24(double *state, double *unused, double *out_8877922091574990347);
void car_H_24(double *state, double *unused, double *out_4978307152328753207);
void car_h_30(double *state, double *unused, double *out_5761472949166298140);
void car_H_30(double *state, double *unused, double *out_6763526167646040238);
void car_h_26(double *state, double *unused, double *out_6429446402584206222);
void car_H_26(double *state, double *unused, double *out_7549719178899592212);
void car_h_27(double *state, double *unused, double *out_4399552238525327924);
void car_H_27(double *state, double *unused, double *out_4588762855845615327);
void car_h_29(double *state, double *unused, double *out_7683597856882407831);
void car_H_29(double *state, double *unused, double *out_7273757511960432422);
void car_h_28(double *state, double *unused, double *out_2603210465267737855);
void car_H_28(double *state, double *unused, double *out_9209356290183792943);
void car_h_31(double *state, double *unused, double *out_4463804505564019373);
void car_H_31(double *state, double *unused, double *out_6923511076666240736);
void car_predict(double *in_x, double *in_P, double *in_Q, double dt);
void car_set_mass(double x);
void car_set_rotational_inertia(double x);
void car_set_center_to_front(double x);
void car_set_center_to_rear(double x);
void car_set_stiffness_front(double x);
void car_set_stiffness_rear(double x);
}