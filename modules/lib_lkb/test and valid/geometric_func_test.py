# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 14:49:12 2015

***REMOVED***
"""

from sys import path

path.append("../../lib_lkb/")

import numpy as np
from geometric_func import *

#############################################################################
#                         TESTING
#############################################################################

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Create satellite and transponder
nadir = np.array([0, 0.0])
distance = 1200
orbit = 'poles'
antenna_tgt_ctr = np.array([0, 0])  # Antenna target Center
beamwidth_a1 = 26.8 * np.pi / 180  # 1.4*np.pi/180 # beam width in degrees
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>







flag_graphic = 1;

if flag_graphic:
    import matplotlib.pyplot as plt

########### TEST 0 : LLgeocentric to ECEF and back #################################

lon = np.arange(-180.0, 181, 10)
lat = np.arange(-90.0, 91, 10)

(xx, yy) = np.meshgrid(lon, lat)

xx_f = xx.flatten()
yy_f = yy.flatten()
# plt.plot(xx_f,yy_f,'.')
# plt.show()

# vect_erf = ll_geod2ecef(np.array([xx_f,yy_f]))
vect_erf = ll_geoc2ecef(np.array([xx_f, yy_f]))

# vect_lonlat = ecef2ll_geod(vect_erf)
vect_lonlat = ecef2ll_geoc(vect_erf) * 180 / np.pi

if flag_graphic:
    erf_x = np.reshape(vect_erf[0, :], xx.shape)
    erf_y = np.reshape(vect_erf[1, :], xx.shape)
    erf_z = np.reshape(vect_erf[2, :], xx.shape)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #    ax.plot_wireframe(vect_erf[:,0],vect_erf[:,1],vect_erf[:,2], linewidth=0.25)
    ax.plot_wireframe(erf_x, erf_y, erf_z, linewidth=0.25)
# ax.plot_surface(erf_x,erf_y,erf_z,rstride=1, cstride=1, color='b')
#    ax.scatter(erf_x,erf_y,erf_z)

###########################################################################



########## TEST 1 : LLgeodetic to ECEF and back #################################

# lon = np.arange(-180.0,181,10)
# lat = np.arange(-90.0,91,10)
#
# (xx,yy) = np.meshgrid(lon,lat)
#
# xx_f = xx.flatten()
# yy_f = yy.flatten()
##plt.plot(xx_f,yy_f,'.')
##plt.show()
#
##vect_erf = ll_geod2ecef(np.array([xx_f,yy_f]))
# vect_erf = ll_geod2ecef(np.array([xx_f,yy_f]))
#
##vect_lonlat = ecef2ll_geod(vect_erf)
# vect_lonlat = ecef2ll_geod(vect_erf)
#
#
#
# if flag_graphic:
#    
#    erf_x = np.reshape(vect_erf[0,:],xx.shape)
#    erf_y = np.reshape(vect_erf[1,:],xx.shape)
#    erf_z = np.reshape(vect_erf[2,:],xx.shape)
#    fig = plt.figure()
#    ax = fig.add_subplot(111, projection='3d')
##    ax.plot_wireframe(vect_erf[:,0],vect_erf[:,1],vect_erf[:,2], linewidth=0.25)
#    ax.plot_wireframe(erf_x,erf_y,erf_z,linewidth=0.25)
##    ax.plot_surface(erf_x,erf_y,erf_z,rstride=1, cstride=1, color='b')
##    ax.scatter(erf_x,erf_y,erf_z)

##########################################################################




########### TEST 2 : LLgeodetic to ECEF #################################
#
#
#
##<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
## Compute Sat properties
# nadir_ecef = ll_geod2ecef(nadir)
# sat_pos = compute_sat_position(nadir_ecef, distance)
# normal_vector = compute_normal_vector(orbit, nadir_ecef)
# mat_passage = compute_sc_coord_vectors(nadir_ecef, sat_pos, normal_vector)
# nadir_sc = np.dot(mat_passage, nadir_ecef - sat_pos) # result should be : nadir_sc = np.array([0,0,35786000])
# az_elev = compute_az_elev(nadir_sc)
#
# if flag_graphic:
#    ax.scatter(nadir_ecef[0],nadir_ecef[1],nadir_ecef[2], c='g',marker ='^')
##<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#
##<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
## Verify by coming back to ECEF coord. system
# uvw = az_elev_2_unitary_uvw(az_elev)
##uvw = np.array([nadir_sc / sum(nadir_sc*nadir_sc)**0.5])
# ecef_unit = np.dot(mat_passage.transpose(),uvw) #+ np.array([sat_pos]).transpose()
# ecef_unit = ecef_unit / sum(ecef_unit*ecef_unit)**0.5
# xyz = compute_intersection_WGS84_ecef(ecef_unit.transpose(), sat_pos)
# diff1 = nadir_ecef - xyz.transpose()
##<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#
#
##<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
## Compute an antenna beam contour
# ant_tgt_ctr_ecef = ll_geod2ecef(antenna_tgt_ctr)
# ant_tgt_ctr_sc = np.dot(mat_passage, ant_tgt_ctr_ecef - sat_pos)
# az_elev_a1 = compute_az_elev(ant_tgt_ctr_sc)
# beam_ctr_a1 = compute_beam_contour(az_elev_a1, beamwidth_a1)
#
## quick graphic verif
##import matplotlib.pylab as plt
##plt.plot(beam_ctr_a1[:,0], beam_ctr_a1[:,1], '.')
##plt.show()
##<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#
##<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
## verify antenna is correct by coming back to ECEF
#
##first for antenna target center
# verif_ant_tgt_ctr_uvw = az_elev_2_unitary_uvw(az_elev_a1)
# verif_ant_tgt_ctr_ecef_unit = np.dot(mat_passage.transpose(),verif_ant_tgt_ctr_uvw)
# verif_ant_tgt_ctr_xyz = compute_intersection_WGS84_ecef(verif_ant_tgt_ctr_ecef_unit.transpose(), sat_pos)
# diff_a1 = ant_tgt_ctr_ecef - verif_ant_tgt_ctr_xyz.transpose()
#
# if flag_graphic:
#    ax.scatter(ant_tgt_ctr_ecef[0],ant_tgt_ctr_ecef[1],ant_tgt_ctr_ecef[2],c='r',marker ='^')
##<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#
#
#
#
##<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
##compute and display beam in ecef
# beam_ctr_a1_uvw = az_elev_2_unitary_uvw(beam_ctr_a1)
# beam_ctr_a1_ecef_unit = np.dot(mat_passage.transpose(),beam_ctr_a1_uvw)
# beam_ctr_a1_xyz = compute_intersection_WGS84_ecef(beam_ctr_a1_ecef_unit, sat_pos)
# beam_ctr_a1_lonlat =  ecef2ll_geod(beam_ctr_a1_xyz)
#
#
# if flag_graphic:
#    ax.plot_wireframe(beam_ctr_a1_xyz[0], beam_ctr_a1_xyz[1], beam_ctr_a1_xyz[2], color = 'r', linewidth=3)
#    ctr = 0
#    # plot rays from satellite
#    while ctr < np.size(beam_ctr_a1_xyz,1):
#        
#        ax.plot(np.array([beam_ctr_a1_xyz[0,ctr],sat_pos[0]]), \
#                np.array([beam_ctr_a1_xyz[1,ctr],sat_pos[1]]), \
#                np.array([beam_ctr_a1_xyz[2,ctr],sat_pos[2]]), color = 'r', linewidth=0.25)
#        ctr += 1
#
##<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

if flag_graphic:
    ax.set_aspect('equal')
    plt.show()


# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_wireframe(beam_ctr_a1_uvw[0], beam_ctr_a1_uvw[1], beam_ctr_a1_uvw[2], color = 'r', linewidth=3)
# plt.show()
