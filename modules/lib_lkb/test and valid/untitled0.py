# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 10:50:15 2015

***REMOVED***
"""

from sys import path

path.append("../../lib_lkb/")

import numpy as np
from geometric_func import *

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Create satellite and transponder
nadir = np.array([0.0, 85.0])
distance = np.array([1200])
inclination_angle = np.array([0.0])  # degs
orbit = 'poles'
antenna_tgt_ctr = np.array([0, 0])  # Antenna target Center
beamwidth_a1 = 26.8 * np.pi / 180  # 1.4*np.pi/180 # beam width in degrees
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Compute Sat properties
# nadir_ecef = ll_geod2ecef(nadir)
# sat_pos = compute_sat_position(nadir_ecef, distance)
# normal_vector = compute_normal_vector(orbit, nadir_ecef)
# normal_vector2 = compute_normal_vector2(inclination_angle*np.pi/180, nadir_ecef)
# mat_passage = compute_sc_coord_vectors(nadir_ecef, sat_pos, normal_vector)
# nadir_sc = np.dot(mat_passage, nadir_ecef - sat_pos) # result should be : nadir_sc = np.array([0,0,35786000])
# az_elev = compute_az_elev(nadir_sc)



import matplotlib.pyplot as plt

########## TEST 1 : LLgeodetic to ECEF and back #################################

lon = np.arange(-180.0, 180.0, 10)
lat = np.arange(-90.0, 90.0, 10)

(xx, yy) = np.meshgrid(lon, lat)

xx_f = xx.flatten()
yy_f = yy.flatten()
# plt.plot(xx_f,yy_f,'.')
# plt.show()

vect_erf = ll_geod2ecef(np.array([xx_f, yy_f]))

vect_lonlat = ecef2ll_geod(vect_erf)

erf_x = np.reshape(vect_erf[0, :], xx.shape)
erf_y = np.reshape(vect_erf[1, :], xx.shape)
erf_z = np.reshape(vect_erf[2, :], xx.shape)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_wireframe(erf_x, erf_y, erf_z, linewidth=0.25)

# ax.scatter(nadir_ecef[0],nadir_ecef[1],nadir_ecef[2], c='g',marker ='x')
#
# ax.scatter(sat_pos[0], sat_pos[1], sat_pos[2])
#
# ax.plot_wireframe(np.array([0,sat_pos[0]]), np.array([0,sat_pos[1]]), np.array([0,sat_pos[2]]))
##########################################################################

# ax.quiver(nadir_ecef[0],nadir_ecef[1],nadir_ecef[2],normal_vector[0],normal_vector[1],normal_vector[2],
# length=1000, color = 'r')
# ax.quiver(nadir_ecef[0],nadir_ecef[1],nadir_ecef[2],normal_vector2[0],normal_vector2[1],normal_vector2[2],
# length=1000, color = 'g')
