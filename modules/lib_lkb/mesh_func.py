# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 17:51:42 2015

***REMOVED***
"""
import numpy as np
from matplotlib.path import Path

#-----------------------------------------------------------------------------#
def mesh_zone(contour_zone, step):
    """
    
    This function takes as an input a contour represented by a 2D array on (lon,lat) values (columnwise)
    and a step which represents half the cell size
    It outputs the meshing of the smallest squared zone completely recovering the contour in input, as a 2D array
    
    """
    # Hypothesis : contour_zone is a 2D vector of (lon,lat)
    lon_ul_corner             =   min(contour_zone[:,0]) # longitude upper left corner
    lat_ul_corner             =   max(contour_zone[:,1]) # latitude upper left corner

    lon_lr_corner             =   max(contour_zone[:,0]) # longitude lower right corner
    lat_lr_corner             =   min(contour_zone[:,1]) # latitude  lower right corner
    
    # we correct lon and lat in order to make sure that the grid is correct with the (0,0) reference
    lon_ul_corner_corrected   =   np.floor(lon_ul_corner / step) * step;
    lat_ul_corner_corrected   =   np.ceil(lat_ul_corner / step) * step;
    lon_lr_corner_corrected   =   (np.ceil(lon_lr_corner / step)+1) * step;
    lat_lr_corner_corrected   =   (np.floor(lat_lr_corner / step )+1) * step;
    
    # meshgrid
    vector_x                  =   np.arange(lon_ul_corner_corrected, lon_lr_corner_corrected, step)
    vector_y                  =   np.arange(lat_ul_corner_corrected, lat_lr_corner_corrected, -step)
    
    return np.meshgrid(vector_x, vector_y)
   # xx_flat = xx.flatten()
   # yy_flat = yy.flatten()
   # return xx_flat, yy_flat

#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
def interp_2D_grids(xx_in, yy_in, zz_in, xx_out, yy_out, resol_grid_in, resol_grid_out, option_flag):
    """ interpolates the values of an a priori irregular input grid, on an a priori irregular too output grid
    
    Example : mapping population grid to a given working grid
    
    Takes into account three options :
    - Surface mean
    - Maximum value
    - Barycenter
    
    
    """
    #first flatten grids
    in_flat = np.vstack([xx_in.flatten(),yy_in.flatten(), zz_in.flatten()])
    out_flat = np.vstack([xx_out.flatten(),yy_out.flatten()])
    in_flat = in_flat.transpose()
    out_flat = out_flat.transpose()
    
    #main function
    loop_ctr = 0
    out_flat_values = np.zeros((np.size(out_flat, 0),1))
    # loop on every point of the output grid
    for loop_ctr in np.arange(0,np.size(out_flat,0),1):
        curr_lon = out_flat[loop_ctr,0]
        curr_lat = out_flat[loop_ctr,1]
        #TODO : check if for loop cannot be enhanced (use nditer)
        
        #first check in input grid which points are covered by the current cell
        points_selected = select_points_covered(in_flat, curr_lon, curr_lat, \
                                                resol_grid_in, resol_grid_out)
        

        
        # then apply correct treatment depending on option chosen
        out_flat_values[loop_ctr,0] = compute_value_grid_cells_selected(curr_lon, curr_lat, resol_grid_in, resol_grid_out, points_selected, option_flag)
        print(loop_ctr)
    zz = np.reshape(out_flat_values,(np.size(xx_out,0),np.size(xx_out,1)))
    return zz
    #finally reshape result under the form of a grid    
#-----------------------------------------------------------------------------#    
    

#_____________________________________________________________________________#
def select_points_covered(in_flat, curr_lon, curr_lat, resol_grid_in, resol_grid_out):
    """ cherche l'ensemble des points qui se trouvent dans la zone du point courant
    Attention ; la grille doit être triée en lon/lat au préalable
    TODO : use masked arrays ?? 
    """
    pos_candidates    = np.logical_and(np.logical_and( \
    in_flat[:,0] < curr_lon + (resol_grid_out/2 + resol_grid_in/2), \
    in_flat[:,0] > curr_lon - (resol_grid_out/2 + resol_grid_in/2)), np.logical_and( \
    in_flat[:,1] < curr_lat + (resol_grid_out/2 + resol_grid_in/2), \
    in_flat[:,1] > curr_lat - (resol_grid_out/2 + resol_grid_in/2)))


    #% on extrait les points de la grille
    return  in_flat[pos_candidates,:]  
#_____________________________________________________________________________#

#_____________________________________________________________________________#
def compute_value_grid_cells_selected(curr_lon, curr_lat, resol_grid_in, resol_grid_out, points_selected, option_flag):
    #check if array is empty
#    pass

    # OPTION 1 & 2 : SURFACE MEAN
    loop_ctr = 0
    ratio_surface = np.zeros((np.size(points_selected,0),1))
    # loop over each selected point
    for loop_ctr in np.arange(0,np.size(points_selected,0),1):
    
        distance_points_lon = np.abs(curr_lon - points_selected[loop_ctr,0])
        distance_points_lat = np.abs(curr_lat - points_selected[loop_ctr,1])    
            
        #first compute for each cell the percentage of overlap with current cell in output grid
    #        %======= Calcul de la zone d'intersection en longitude ========
            
    #        % si la zone du point de grille d'entree est à l'interieur de la zone
    #        % du point de grille de sortie
        if (np.logical_and(resol_grid_in /2  < resol_grid_out / 2, distance_points_lon + resol_grid_in/2 < resol_grid_out/2)):
            lon_a_considerer = resol_grid_in            
    #            % si la zone du point de grille de sortie est à l'interieur de la zone
    #            % du point de grille d'entrée
        elif (np.logical_and(resol_grid_out/2 < resol_grid_in/2, distance_points_lon + resol_grid_out/2 < resol_grid_in/2)):            
            lon_a_considerer = resol_grid_out            
    #            % si intersection
        else:            
            lon_a_considerer = resol_grid_out/2 + resol_grid_in/2 - distance_points_lon
            
    #        %======= Calcul de la zone d'intersection en latitude ==========        
    #        % si la zone du point de grille d'entree est à l'interieur de la zone
    #        % du point de grille de sortie
        if (np.logical_and(resol_grid_in/2 < resol_grid_out/2, distance_points_lat + resol_grid_in/2 < resol_grid_out/2)):            
            lat_a_considerer = resol_grid_in;            
    #            % si la zone du point de grille de sortie est à l'interieur de la zone
    #            % du point de grille d'entrée
        elif (np.logical_and(resol_grid_out/2 < resol_grid_in/2, distance_points_lat + resol_grid_out/2 < resol_grid_in/2)):            
            lat_a_considerer = resol_grid_out            
    #            % si intersection
        else:            
            lat_a_considerer = resol_grid_out/2 + resol_grid_in/2 - distance_points_lat
                
            
            
    #        % on détermine le rapport de la surface du point de la grille
    #        % d'entrée qui se trouve dans la zone du point courant de la grille
    #        % d'entrée
#        rapport_surface_a_prendre_en_compte = 1/(resol_grid_in)**2 * lon_a_considerer * lat_a_considerer    
        ratio_surface[loop_ctr,0]= 1/(resol_grid_in)**2 * lon_a_considerer * lat_a_considerer
        
#        
         
    if (option_flag == 'moyenne_surface'): # OPTION Moyenne surfacique
        result = np.sum(ratio_surface.transpose() * points_selected[:,2])
#            
    elif (option_flag == 'max'): # OPTION Maximum value represented in cell
        curr_score = 0
        new_score = 0
        possible_vals = np.unique(points_selected[:,2])
        loop_pos_vals = 0
        for loop_pos_vals in np.arange(0,np.size(possible_vals,0),1):
            new_score = np.sum(ratio_surface[points_selected[:,2] == possible_vals[loop_pos_vals]])
            if new_score > curr_score:
                curr_score = new_score                
                result = possible_vals[loop_pos_vals]

    return result
#_____________________________________________________________________________#





#-----------------------------------------------------------------------------#
def assign_contours_to_points(lon,lat,contour):
    """
     This function assign to each point a contour_id
     It takes as an input :
     - a grid of (lon, lat) (typically obtained with meshgrid)
     - a list of contours (what about their IDs ??? - already sorted or added as dictionnary TBC)
     """
     #TODO : change and work directly from flattened
     # flatten (lon,lat) grid    
    lon_lat = np.vstack([lon,lat])
    lon_lat = lon_lat.transpose()
    result = np.ones((np.size(lon_lat,0),1)) * -9999;    
    loop_ctr=1
    
    # check which (lon,lat) are contained in contour and assign it id
    pth = Path(contour)
    mask = pth.contains_points(lon_lat)
    result[mask] = loop_ctr
    val_debug = np.sum(mask)
    loop_ctr += 1
        
        # look at masked arrays
    return mask
    
 #-----------------------------------------------------------------------------#









##-----------------------------------------------------------------------------#
#def assign_contours_to_points(xx,yy,contours):
#    """
#    This function assign to each point a contour_id
#    It takes as an input :
#    - a grid of (lon, lat) (typically obtained with meshgrid)
#    - a list of contours (what about their IDs ??? - already sorted or added as dictionnary TBC)
#    """
#    #TODO : change and work directly from flattened
## flatten (lon,lat) grid    
#    lon_lat = np.vstack([xx.flatten(),yy.flatten()])
#    lon_lat = lon_lat.transpose()
#    result = np.ones((np.size(lon_lat,0),1)) * -9999;    
#    loop_ctr=1
#    
#    for item in contours:
#        
#        # check which (lon,lat) are contained in contour and assign it id
#        pth = Path(contours[item])
#        mask = pth.contains_points(lon_lat)
#        result[mask] = loop_ctr
#        
#        loop_ctr += 1
#        
#        # look at masked arrays
#    return np.reshape(result,np.shape(xx))
#    
##-----------------------------------------------------------------------------#


































#############################################################################
#SCRIPTS TO GENERATE COUNTRY/MAP DATA
#array_cmap = np.loadtxt("C:\\Users\\Damien Roques\\Documents\\technical stuff\\WinPython-64bit-3.3.5.0\\python-3.3.5.amd64\\Scripts\\mapping_tool\\country_map\\glbnds.asc",skiprows=6);
#
#np.save("./country_map/array_cmap", array_cmap)


#array_pop = np.loadtxt("C:\\Users\\Damien Roques\\Documents\\technical stuff\\WinPython-64bit-3.3.5.0\\python-3.3.5.amd64\\Scripts\\mapping_tool\\pop_count\\glp15ag.asc",skiprows=6);
#
#np.save("./pop_count/array_pop", array_pop)


##############################################################################















