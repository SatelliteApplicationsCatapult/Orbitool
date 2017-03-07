# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 11:42:39 2015

***REMOVED***
"""

#%%
################################################################################################
#                                 TESTS                                                        #       
################################################################################################

flag_graphic = 1
import numpy as np
from mesh_func import *
import matplotlib.pylab as plt

#%%
##################################################
## TEST 1 : dummy test of 2D interpolation (change paramter between max and moyenne_surface to check both)
#contour_zone = np.array([[0, 0],[10, 10]])
#step = 1
#xx, yy  = mesh_zone(contour_zone, step)
#
#step_2 = 0.2
#aa, bb  = mesh_zone(contour_zone, step_2)
#cc = np.ones((np.size(aa, 0),np.size(aa, 1)))
#
#
#zz = interp_2D_grids(aa, bb, cc, xx, yy, step_2, step, 'max')


#%%
#################################################
# TEST 2 : test of country interpolation on grid

lon_min = -20
lat_min = 20
lon_max = 20
lat_max = 70
contour_zone = np.array([[lon_min, lat_min],[lon_max, lat_max]])
#define output grid
step = 0.2
xx, yy  = mesh_zone(contour_zone, step)

# load country grid and create lon,lat grid
# LOAD DATA
#array_cmap = np.load("./country_map/array_cmap.npy")
array_pop = np.load("./pop_count/array_pop.npy")

# COORD SYSTEM 
#TODO : read from file and check consistency between map and pop files
ncols        =   8640
nrows        =   3432
xllcorner    =   -180
yllcorner    =   -58
cellsize     =   0.0416666666667
NODATA_value =   -9999



# build (lon,lat) matrices with meshgrid
x_vector     =   np.arange(xllcorner,180.0000,cellsize)
#x_vector     =   np.linspace(xllcorner,cellsize,ncols)
y_vector     =   np.arange(yllcorner,85,cellsize) # value of 85 found out empirically
#y_vector     =   np.fliplr(y_vector)


aa,bb        =   np.meshgrid(x_vector,y_vector)
bb           =   np.flipud(bb)

ind_lon_min = np.nonzero(aa[0,:]>=lon_min-step-cellsize)[0][0]
ind_lon_max = np.nonzero(aa[0,:]>=lon_max+step+cellsize)[0][0]

ind_lat_min = np.nonzero(bb[:,0]<=lat_min-step-cellsize)[0][0]
ind_lat_max = np.nonzero(bb[:,0]<=lat_max+step+cellsize)[0][0]



aa_r = aa[ind_lat_max:ind_lat_min, ind_lon_min:ind_lon_max]
bb_r = bb[ind_lat_max:ind_lat_min, ind_lon_min:ind_lon_max]
#array_cmap_r = array_cmap[ind_lat_max:ind_lat_min, ind_lon_min:ind_lon_max]
array_pop = array_pop[ind_lat_max:ind_lat_min, ind_lon_min:ind_lon_max]

#import matplotlib.pylab as plt
#plt.contour(aa_r,bb_r,array_cmap_r)
#plt.show()
#plt.set_cmap("prism")
#array_cmap_r[array_cmap_r==-9999] = 0
#plt.pcolor(aa_r,bb_r,array_cmap_r)


#zz = interp_2D_grids(aa_r, bb_r, array_cmap_r, xx, yy, cellsize, step, 'max')
zz = interp_2D_grids(aa_r, bb_r, array_pop, xx, yy, cellsize, step, 'moyenne_surface')

if flag_graphic:
    zz_toplot = zz.copy()
    zz_toplot[zz_toplot==-9999]=0
    zz_toplot[zz_toplot>200000]=200000
    plt.set_cmap("YlOrRd")
    plt.pcolor(xx,yy,zz_toplot)
    plt.show()





#%%
###########################################################################
## TEST 3 : assign point to contour test
#import matplotlib.pylab as plt
#
#lon_min = 0
#lat_min = 0
#lon_max = 10
#lat_max = 10
#
#contour_zone = np.array([[lon_min, lat_min],[lon_max, lat_max]])
##define output grid
#step = 1
#xx, yy  = mesh_zone(contour_zone, step)
#
#sub_contour = {"contour" : np.array([[3, 3],[3, 7],[7,7],[7,3]])}
#
#
#result = assign_contours_to_points(xx,yy,sub_contour)
#
#plt.pcolor(xx,yy,result)
