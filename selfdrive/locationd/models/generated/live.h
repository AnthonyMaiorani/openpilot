#pragma once
#include "rednose/helpers/ekf.h"
extern "C" {
void live_update_4(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_9(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_10(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_12(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_35(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_32(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_13(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_14(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_update_33(double *in_x, double *in_P, double *in_z, double *in_R, double *in_ea);
void live_H(double *in_vec, double *out_3457479244464077531);
void live_err_fun(double *nom_x, double *delta_x, double *out_650718210523216323);
void live_inv_err_fun(double *nom_x, double *true_x, double *out_910473225309207357);
void live_H_mod_fun(double *state, double *out_2181166024205561752);
void live_f_fun(double *state, double dt, double *out_3533239200643131825);
void live_F_fun(double *state, double dt, double *out_5539989427522668852);
void live_h_4(double *state, double *unused, double *out_819859370756235625);
void live_H_4(double *state, double *unused, double *out_2871740975048229748);
void live_h_9(double *state, double *unused, double *out_4802105354618293564);
void live_H_9(double *state, double *unused, double *out_2630551328418639103);
void live_h_10(double *state, double *unused, double *out_7610955400709654716);
void live_H_10(double *state, double *unused, double *out_1974782145108752521);
void live_h_12(double *state, double *unused, double *out_1634941094875625440);
void live_H_12(double *state, double *unused, double *out_2147715432983732047);
void live_h_35(double *state, double *unused, double *out_5460157810480551459);
void live_H_35(double *state, double *unused, double *out_4893278465308745756);
void live_h_32(double *state, double *unused, double *out_5557633069685588267);
void live_H_32(double *state, double *unused, double *out_7752161236193193302);
void live_h_13(double *state, double *unused, double *out_2477464069165319992);
void live_H_13(double *state, double *unused, double *out_8540249629042519317);
void live_h_14(double *state, double *unused, double *out_4802105354618293564);
void live_H_14(double *state, double *unused, double *out_2630551328418639103);
void live_h_33(double *state, double *unused, double *out_327564127954512118);
void live_H_33(double *state, double *unused, double *out_8043835469947603360);
void live_predict(double *in_x, double *in_P, double *in_Q, double dt);
}