# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 21:25:04 2015

***REMOVED***
"""
import numpy as np
import logging
logger = logging.getLogger("web2py.app.myweb2pyapplication")
logger.setLevel(logging.DEBUG)

# -----------------------------------------------------------------------------
def ll_geoc2ecef(lon_lat_vect):
    '''
    THis function converts GEOCENTRIC lon/lat points into ECEF (x,y,z) system of coordinates, for X points
    simultaneously
    
    Input  : 
        - lon_lat_vect : [2,X] array of lon, lat IN DEGREES 
    Output : 
        - position of points in ECEF : [3,X] array of (x,y,z)ecef in kms
    
    '''

    # 	Constant definitions

    RTE = 6378.1370  # % equatorial radius RTE (km)

    #    # <><><><><> Consistency <><><><>
    #    # force type to float (in case this was an integer)
    #    lon_lat_vect = lon_lat_vect.astype('float')
    #    # <><><><><> /Consistency <><><><>

    # % convert lon, lat  and lonsat into radians
    lon = lon_lat_vect[0]
    lat = lon_lat_vect[1]
    lon = lon / 180 * np.pi
    lat = lat / 180 * np.pi

    x = RTE * np.cos(lat) * np.cos(lon)
    z = RTE * np.sin(lat)
    y = RTE * np.cos(lat) * np.sin(lon)

    return np.array([x, y, z])


# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
def ecef2ll_geoc(points_list):
    """
    This functions converts ECEF coordinates into lon/lat GEOCENTRIC, under the assumption
    that points are at altitude 0, for X points simultaneously
    Input  : 
        - points_list : [3,X] array of (x,y,z)ecef in kms
    Output : 
        - position of points in lon/lat : [2,X] array of (lon,lat) in degrees
    
    """

    x = points_list[0]
    y = points_list[1]
    z = points_list[2]

    lat = np.arcsin(z / np.sqrt(x * x + y * y + z * z))
    lon = np.arctan2(y, x)

    return np.array([lon, lat])

    # TO VALIDATE !!


# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def ll_geod2ecef(lon_lat_vect):
    '''
    THis function converts GEODETIC (WGS84) lon/lat point into ECEF (x,y,z) system of coordinates, for X points
    simultaneously
    
    Input  : 
        - lon_lat_vect : [2,X] array of lon, lat IN DEGREES 
    Output : 
        - position of points in ECEF : [3,X] array of (x,y,z)ecef in kms
    
    '''

    # 	Constant definitions

    RTE = 6378.1370  # % equatorial radius RTE (km)
    RTP = 6356.7523  # % pole radius RTP (km)

    # % convert lon, lat  and lonsat into radians
    lon = lon_lat_vect[0]
    lat = lon_lat_vect[1]
    lon = lon / 180 * np.pi
    lat = lat / 180 * np.pi

    # % Calculate the (x,y,z)erf coordinates :

    e2 = (RTE ** 2 - RTP ** 2) / (RTE ** 2);

    Rn = RTE / (np.sqrt(1 - e2 * (np.sin(lat)) ** 2));

    return np.array([Rn * np.cos(lat) * np.cos(lon), \
                     Rn * np.cos(lat) * np.sin(lon), \
                     Rn * (1 - e2) * np.sin(lat)])


# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def ecef2ll_geod(points_list):
    """
    This functions converts ECEF coordinates into lon/lat GEODETIC (WGS 84), under the assumption
    that points are at altitude 0, for X points simultaneously
    
    Input  : 
        - points_list : [3,X] array of (x,y,z)ecef in kms
    Output : 
        - position of points in lon/lat : [2,X] array of (lon,lat) in degrees
    
    """
    RTE = 6378.1370  # e3	#				% equatorial radius RTE (km)
    RTP = 6356.7523  # e3	#			% pole radius RTP (km)

    x = points_list[0]
    y = points_list[1]
    z = points_list[2]

    lon = np.ones(np.size(x)) * np.nan
    lat = np.ones(np.size(x)) * np.nan

    # Compute lon
    lon[np.atleast_1d(x ** 2 + y ** 2 > 1e-06)] = np.arctan2(y, x)[x ** 2 + y ** 2 > 1e-06]
    lon[np.atleast_1d(x ** 2 + y ** 2 <= 1e-06)] = 0

    #	Compute lat (iterations not needed since h = 0 (checked experimentally only))
    e2 = (RTE ** 2 - RTP ** 2) / (RTE ** 2)
    k_i = 1 / (1 - e2)

    lat = np.arctan(k_i * z / np.sqrt(x ** 2 + y ** 2))
    lat = lat * 180 / np.pi
    lon = lon * 180 / np.pi

    return np.array([lon, lat])


# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def compute_ecef_2_sc_nominal(vect_ecef, nadir_ecef, sat_pos_ecef, normal_vector):
    '''
    Description TODO: switch from ECEF to SC nominal
    
    Note : also works with one satellite only
    '''

    # compute matrix to go to SC coord. system
    # TODO : create optional parameter for matrix (if has been computed already)
    mat_ecef2sat = compute_ecef_2_sc_rot_matrix(nadir_ecef, sat_pos_ecef,
                                                normal_vector)  # rotation matrix to go to SAT coordinate system

    vect_to_mult = (vect_ecef.T - sat_pos_ecef.T).T  # apply translation
    # TODO : change the ugly tranpose (this is to handle 1D vectors)

    return multi_matrix_product(mat_ecef2sat, vect_to_mult)


#    # case with 1D vectors
#    if sat_pos_ecef.ndim == 1:
#        points_sat_coord = np.dot(mat_ecef2sat, (vect_ecef.T - sat_pos_ecef.T).T) #TODO : change the ugly tranpose (
# this is to handle 1D vectors)
#
#        
#    else:
#    
#        # matrix calculation using np.einsum
#        #( replaces code found on Internet :
# https://jameshensman.wordpress.com/2010/06/14/multiple-matrix-multiplication-in-numpy/)
#         vect_to_mult = (vect_ecef.T - sat_pos_ecef.T).T #TODO : change the ugly tranpose
#         points_sat_coord = np.einsum('ij...,j...',mat_ecef2sat,vect_to_mult).T       


#    return points_sat_coord
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
def compute_coord_system_rotation(points_to_rotate, x_angle, y_angle, z_angle):
    '''
    Description : TODO go grom sc_nominal to sc_tilted coord. system
    '''
    # TODO : handle here additional cases where we already have a matrix
    # (therefore no need for angles and no need to compute it)
    rot_mat = compute_xyz_rot_matrices(-x_angle, -y_angle, -z_angle)

    # matrix product of many matrices
    points_rotated = multi_matrix_product(rot_mat, points_to_rotate)

    return points_rotated


# -----------------------------------------------------------------------------

##-----------------------------------------------------------------------------        
# def compute_sc_nominal_2_sc_tilted(points_sat_coord, roll, pitch, yaw):
#    '''
#    Description : TODO go grom sc_nominal to sc_tilted coord. system
#    '''
#    #Note : minus because the rotation matrix defines rotation and not change of coord. system
#    rpy_mat = compute_xyz_rot_matrices(roll, pitch, yaw)
#    
#
#    # matrix product of many matrices
#    points_sat_coord_tilted = multi_matrix_product(rpy_mat, points_sat_coord)    
#    
#    
##    
##    points_sat_coord_tilted = np.einsum('ij...,j...',rpy_mat,points_sat_coord).T
##
##    
##
##    #<><><><><><> Consistency <><><><><><><>
##    if points_sat_coord.ndim == 1:
##        points_sat_coord_tilted = np.reshape(points_sat_coord_tilted, (3))
##    #<><><><><><> Consistency <><><><><><><>
#    
#    return points_sat_coord_tilted
#    
##----------------------------------------------------------------------------- 


##-----------------------------------------------------------------------------        
# def compute_sc_tilted_2_ant(points_sat_coord_tilted, x_angle, y_angle, z_angle):
#    '''
#    Description : TODO go grom sc_nominal to sc_tilted coord. system
#    '''
#    #Note : minus because the rotation matrix defines rotation and not change of coord. system
#    rot_mat = compute_xyz_rot_matrices(x_angle, y_angle, z_angle)
#    
#
#    # matrix product of many matrices
#    points_sat_coord_tilted = multi_matrix_product(rot_mat, points_sat_coord_tilted)    
#    
#
#    
#    return points_sat_coord_tilted
##-----------------------------------------------------------------------------        


# -----------------------------------------------------------------------------
def compute_az_elev(point_list):
    """
    compute azimuth and elevation of X points compared to axis z (0,0,1)
    
    Input  : 
        - point_list : [3,X] array of (x,y,z) 3D coord values (e.g. (sc) for satellite antenna, e.g. in kms) 
    Output : 
        - [2,X] array of (az, elev)  in radians
    
    """

    elev = np.arcsin(point_list[1] / (np.sum(point_list * point_list, axis=0) ** 0.5))
    az = np.arctan2(point_list[0], point_list[2])

    #   treatment of elevations > 180 deg.    ==> should not be useful
    #   elev(elev > (np.pi/2)) = np.pi - elev(elev > (np.pi/2))

    return np.array([az, elev])


# -----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
def az_elev_2_unitary_uvw(az_elev_list):
    """computes X unitary vectors (u,v,w) from azimuth and elevation
    Note that vectors have to be unitary since 'depth' info is lost with az_elev
    Input  : 
        - az_elev_list : [2,X] array of (azimuth, elevation) in radians
        
    Output : 
        - [3,X] array of unitary vectors (u,v,w) in 3D coord. system (e.g. SC for sat_antenna or ECEF for ground
        antennas, e.g. in kms)
    """

    # get back to x,y,z


    x = np.tan(az_elev_list[1]) * np.cos(az_elev_list[0])
    y = np.tan(az_elev_list[1]) * np.sin(az_elev_list[0])

    if np.ndim(az_elev_list) == 1:
        z = 1.0
    else:
        z = np.ones(np.size(az_elev_list, 1)) * 1.0

    #    x = np.tan(az_elev_list[0])
    #    y = np.tan(az_elev_list[1]) * np.sqrt(x**2 + z**2)

    #    x = np.cos(az_elev_list[1]) * np.sin(az_elev_list[0])
    #    y = np.sin(az_elev_list[1])
    #    z = np.cos(az_elev_list[1]) * np.cos(az_elev_list[0])



    # norm the vector
    #    norm_xyz = (x**2+y**2+z**2)**0.5
    #    x = x/norm_xyz
    #    y = y/norm_xyz
    #    z = z/norm_xyz
    #
    return np.array([x, y, z])


# ----------------------------------------------------------------------------


##-----------------------------------------------------------------------------        
# def compute_ant_2_sc_tilted(points_ant_coord, x_angle, y_angle, z_angle):
#    '''
#    Description : TODO go grom sc_nominal to sc_tilted coord. system
#    '''
#    #TODO : handle here additional cases where we already have a matrix
#    # (therefore no need for angles and no need to compute it)
#    rot_mat = compute_xyz_rot_matrices(-x_angle, -y_angle, -z_angle)
#    
#
#    # matrix product of many matrices
#    points_sat_coord_tilted = multi_matrix_product(rot_mat, points_ant_coord)    
#    
#
#    
#    return points_sat_coord_tilted
#
##-----------------------------------------------------------------------------        


##-----------------------------------------------------------------------------        
# def compute_sc_tilted_2_sc_nominal(points_sat_coord, roll, pitch, yaw):
#    '''
#    Description : TODO go grom sc_nominal to sc_tilted coord. system
#    '''
#    #Note : minus because the rotation matrix defines rotation and not change of coord. system
#    rpy_mat = compute_xyz_rot_matrices(-roll, -pitch, -yaw)
#    
#    
#    # matrix product of many matrices
#    points_sat_coord_nominal = multi_matrix_product(rpy_mat, points_sat_coord)     
#    
#    
#    
##    points_sat_coord_nominal = np.einsum('ij...,j...',rpy_mat,points_sat_coord).T
##
##
##    #<><><><><><> Consistency <><><><><><><>
##    if points_sat_coord.ndim == 1:
##        points_sat_coord_nominal = np.reshape(points_sat_coord_nominal, (3))
##    #<><><><><><> Consistency <><><><><><><>
#    
#    return points_sat_coord_nominal
#    
##-----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def compute_unitary_uvw_2_ecef(vect_sat, nadir_ecef, sat_pos_ecef, normal_vector):
    '''
    Description TODO: switch from uvw to ecef
    '''

    # first compute the UVW vectors coord. in ecef coordinates (note that this is NOT the position in ECEF)
    vect_unit_ecef = compute_uvw_sc_nominal_2_unitary_ecef(vect_sat, nadir_ecef, sat_pos_ecef, normal_vector)

    # then compute points position by taking the intersection with the ellipsoid (or sphere)    
    # TODO : add option for sphere
    return compute_intersection_WGS84_ecef(vect_unit_ecef, sat_pos_ecef)


# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def compute_elev_grd(pos_station, pos_sat):
    """
    Computes elevation of X ground stations, pointing at X satellites  : 
    (Note : this works also if only one satellite is used for the X points)
    
    Input :
        - pos_station : [3,X] stations positions in 3D coord. system (e.g. ECEF, in kms)
        - pos_sat : [3,X] OR [3,1] ARRAY of satellite position in 3D coord. system (e.g. ECEF, in kms)
  
    
    Output : 
        - [X] vector of elevations in degrees (?)
    """

    # TODO : merge with function above
    vect_dir_sat = (pos_sat.transpose() - pos_station.transpose()).transpose()

    cos_angle = np.atleast_1d(
        np.sum(pos_station * vect_dir_sat, axis=0) / (np.sum(pos_station * pos_station, axis=0) ** 0.5 * \
                                                      np.sum(vect_dir_sat * vect_dir_sat, axis=0) ** 0.5))

    # round to avoid extreme cases
    cos_angle = np.round(cos_angle, decimals=8)
    #    cos_angle[cos_angle<-1]= -1.0

    arcos_angle = np.arccos(cos_angle)
    arcos_angle[np.isnan(arcos_angle)] = 0

    elev = (np.pi / 2 - arcos_angle) * 180 / np.pi

    elev[elev < 0] = 0

    return elev


# -----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
def compute_beam_contour(az_elev, beamwidth):
    """ computes a circle of radius equal to "beamwidth" in radians, around a center 
        Input  : 
            - az_elev : [2,X] array of (azimuth, elevation) in radians (?)
            - beamwidth : [X] array of beamwidths
            
        Output :
            - [2,X] ??? array of (az,elev) points on the circle in radians
            
    """

    azimuth = np.arange(0, 2 * np.pi, 0.1)
    elevation = np.ones(np.size(azimuth)) * beamwidth

    beam = np.array([azimuth, elevation])

    #    iter_vect = np.arange(0,2*np.pi,0.1)
    ##    iter_vect = np.arange(0,0.1,0.1)
    #    beam = np.zeros([2,np.size(iter_vect)])
    #    ctr = 0
    #
    #    for theta in  iter_vect:
    #        coord_a = az_elev[0] + beamwidth * np.cos(theta)
    #        coord_b = az_elev[1] + beamwidth * np.sin(theta)
    #
    #        beam[:,ctr] = np.array([coord_a,coord_b])
    #        ctr += 1

    # TODO : what is returned eventually ???
    return beam


# ----------------------------------------------------------------------------




# ----------------------------------------------------------------------------
def compute_ecef_to_az_elev(vect_ecef, \
                            nadir_ecef, \
                            sat_pos_ecef, \
                            normal_vector, \
                            roll=np.nan, \
                            pitch=np.nan, \
                            yaw=np.nan \
                            ):
    ''' Computes all the steps to convert ecef coord. points to azimuth/elevation in Spacecraft (SC) coord.
    NOTE : Two intermediate steps are assumed to be already computed :
        - normal vector of satellite(s) orbit has been computed
        - nadir of satellite(s) has been computed
        Inputs : 
             - vect_ecef : [3,X] array representing ECEF coord. in kms of points to convert
             - sat_pos_ecef : [3, X] array representing ECEF coord. in kms of satellite position
             - nadir_ecef : [3,X] array representing ECEF coord. in kms of nadir
             - normal_vector : [3,X] array representing the vector normal to satellite orbit
             - roll, pitch, yaw : OPTIONAL : [X] vector of roll, pitch, yaw if any, in radians
        
        Output : 
             - [2,X] array of az/elev points
    '''

    # TODO : use different flags and optional params for speed (if matrices are already computed, etc.)

    #     first size arrays as 2D arrays    IS IT USEFUL ? not anymore...
    #    [vect_ecef, nadir_ecef, normal_vector, sat_pos_ecef] = homogenize_arrays_dimensions([vect_ecef, nadir_ecef,
    # normal_vector, sat_pos_ecef])

    #     Go from ECEF to Nominal SpaceCraft Coord. system (without Roll, Pitch, Yaw)
    points_sat_coord = compute_ecef_2_sc_nominal(vect_ecef, nadir_ecef, sat_pos_ecef, normal_vector)

    #    Perform roll,pitch, yaw rotation IF any is specified
    if np.any(np.isnan(roll)):
        points_sat_coord_tilted = points_sat_coord
    else:
        points_sat_coord_tilted = compute_coord_system_rotation(points_sat_coord, roll, pitch, yaw)

    # Azimuth, elevation of points and beam centers
    az_elev_points = compute_az_elev(points_sat_coord_tilted)
    return az_elev_points


# ----------------------------------------------------------------------------




# ----------------------------------------------------------------------------

def compute_az_elev_to_ecef(az_elev, \
                            nadir_ecef, \
                            sat_pos_ecef, \
                            normal_vector, \
                            roll=np.nan, \
                            pitch=np.nan, \
                            yaw=np.nan \
                            ):
    ''' 
    This function converts points from (az, elev) coordinates in Spacecraft (SC) coordinate system, back to ECEF    

    NOTE : Two intermediate steps are assumed to be already computed :
        - normal vector of satellite(s) orbit has been computed
        - nadir of satellite(s) has been computed
        Inputs : 
             - az_elev : [2,X] array representing azimuth and elevation of points on Earth in (SC) coordinates
             - sat_pos_ecef : [3,X] array representing ECEF coord. in kms of satellite positions
             - nadir_ecef : [3,X] array representing ECEF coord. in kms of nadir
             - normal_vector : [3,X] array representing the vector normal to satellite orbit
             - roll, pitch, yaw : OPTIONAL : [X] vector of roll, pitch, yaw if any, in radians
    
        Output :
            - [3,X] array of positions in ECEF (in kms). Note that points are assumed to be ON EARTH (no altitude)
    
    '''

    points_uvw_tilted = az_elev_2_unitary_uvw(az_elev)

    #    Perform roll,pitch, yaw rotation IF any is specified
    if np.any(np.isnan(roll)):
        points_uvw_nominal = points_uvw_tilted
    else:
        points_uvw_nominal = compute_coord_system_rotation(points_uvw_tilted, roll, pitch, yaw)

    return compute_unitary_uvw_2_ecef(points_uvw_nominal, nadir_ecef, sat_pos_ecef, normal_vector)


#    
#    # compute matrix to go to SC coord. system
#    mat_sat = compute_ecef_2_sc_rot_matrix(nadir_ecef, sat_pos_ecef, normal_vector) # rotation matrix to go to SAT
# coordinate system
#
#    # case with 1D vectors
#    if nadir_ecef.ndim == 1:
#        
#        uvw = az_elev_2_unitary_uvw(az_elev)
#        
#        if np.any(np.isnan(roll)):
#            uvw_untilted = uvw
#        else:
#            rpy_mat = compute_xyz_rot_matrices(-roll, -pitch, -yaw)
#            uvw_untilted = np.dot(np.transpose(rpy_mat,(1,0,2)), uvw)
#
#        ecef_unit = np.dot(mat_sat.transpose(),uvw_untilted) #+ np.array([sat_pos]).transpose()
#        ecef_unit = ecef_unit / sum(ecef_unit*ecef_unit)**0.5
#        points_ecef = compute_intersection_WGS84_ecef(ecef_unit.transpose(), sat_pos_ecef)
#        
#    else:
#
#        vect_uvw = az_elev_2_unitary_uvw(az_elev)
#        
#        if np.any(np.isnan(roll)):
#            vect_uvw_untilted = vect_uvw
#        else:
#            rpy_mat = compute_xyz_rot_matrices(-roll, -pitch, -yaw)        
#            # transpose matrix of RPY
#            rpy_mat = np.transpose(rpy_mat,(1,0,2))        
#            vect_uvw_untilted = np.einsum('ij...,j...',rpy_mat,vect_uvw).T
#        
#        # transpose to go from SAT to ECEF
#        mat_sat = np.transpose(mat_sat,(1,0,2))
#        
#        # matrix calculation (smartly done with code found on Internet)
#        # WARNING : the following only works with 2D-defined vectors ! 
#        mat_to_use = np.transpose(mat_sat,(2,0,1))
#        vect_uvw_untilted = vect_uvw_untilted.transpose()
#        
#        vect_uvw_untilted = vect_uvw_untilted.reshape(np.size(nadir_ecef)/3,3,1)
#        points_ecef_unit = np.sum(np.transpose(mat_to_use,(0,2,1)).reshape(np.size(nadir_ecef,1),3,3,
# 1) * vect_uvw_untilted.reshape(np.size(nadir_ecef,1),3,1,1),-3)
#        points_ecef_unit = points_ecef_unit.reshape(np.size(nadir_ecef,1),3).transpose()
#    
#        # compute intersection with WGS 84
#        points_ecef = compute_intersection_WGS84_ecef(points_ecef_unit, sat_pos_ecef)
#    
#         
#    return points_ecef
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# def translate_az_elev_sc_to_az_elev_ant(az_elev_beam_centers, az_elev_points):
#    ''' This function switches from (A,B)SC to (A,B)ANT coordinate system, by setting the center of the
#    set of coordinates, which is the satellite nadir in the case of SC, to the center of the beam (which is the
# center of
#    the ANT cood. system). This is a simple translation. 
#    Note : the function is vectorized for improved fastness'''
#    return  az_elev_points - az_elev_beam_centers   
#    
##----------------------------------------------------------------------------
#    
#    
##----------------------------------------------------------------------------
# def translate_az_elev_ant_to_az_elev_sc(az_elev_beam_centers, az_elev_points):
#    ''' This function switches from (A,B)ANT to (A,B)SC coordinate system. see opposite function (
# translate_az_elev_sc_to_az_elev_ant)
#    for more explanations'''    
#    return  az_elev_points + az_elev_beam_centers
#    
# ----------------------------------------------------------------------------

# ======================================================================================================================
#   SECONDARY FUNCTIONS
# ======================================================================================================================

# ----------------------------------------------------------------------------
def homogenize_arrays_dimensions(list_variables):
    '''
    Checks applied :
    - transform every array into 2D-array
    '''
    counter = 0

    flag_1_elt_is_2D = False

    # check whether one element is in 2D
    for elt in list_variables:
        if elt.ndim == 1:
            flag_1_elt_is_2D = True

    # if one is in 2D, convert the ones not in 2D if any                    
    if flag_1_elt_is_2D:
        for elt in list_variables:
            if elt.ndim == 1:
                list_variables[counter] = np.reshape(elt, (np.size(elt), 1))
            counter += 1

    return list_variables


# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
def check_array_size_consistency(list_variables):
    pass
    # TODO : check all arrays are consistent in terms of size


# ----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def compute_sat_position(nadir, distance):
    ''' returns satellite positions of X satellites
    Input  : 
       - nadir    :  [3,X] array of (x,y,z)ecef in kms
       - distance :  [X] array of distances in kms
    Output : 
       - satellite positions as a [3,X] array of (x,y,z)ecef
    
    NOTE : if only one distance is given (scalar), then the same distance is applied to all nadir points    
    '''

    norm_nadir = np.sum(nadir * nadir, axis=0) ** 0.5

    return (nadir / norm_nadir) * (distance + norm_nadir)


# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def compute_normal_vector(inclination_angle, nadir_ecef, flag_asc_desc):
    ''' this functions computes, for X satellites, the vector normal to the elliptic plan in the case 
    of GEO or meridian orbit. It should be seen as a possible help to build satellite characteristics
    
    Input :
        - inclination_angle : [X] array of inclination angles in radians (?)
        - nadir_ecef : [3,X] array of (x,y,z) nadir_ecef
        - flag_asc_desc : [X] array of flag determining the satellite direction on his orbit ('ASC' or 'DESC')    
    
    Output :
        - normal vector to the orbit (for each satellite) : [3, X] array of normalized vectors
        Note : output is always a 2D array ([3,X] shape)
    '''

    # TODO : clean the function and make sure that if a 1D vector is entered it returns a 1D vector
    # TODO : works only if flag_asc_desc is embedded in an array


    # <><><><><><><><><><><><> Consistency checks <><><><><><><><><><><><><><><><>
    # check if flag_asc_desc is just a string, therefore converts it :
    # TODO : not Python 3.X compatible
    if isinstance(flag_asc_desc, basestring):
        flag_asc_desc = np.array([flag_asc_desc])

    # check if inclination_angle is just a scalar
    if isinstance(inclination_angle, (float, int)):
        inclination_angle = np.array([inclination_angle])

    # check if nadir_ecef is a (3) or (3,X) vector
    flag_output_1D = False
    if nadir_ecef.ndim == 1:
        flag_output_1D = True
        nadir_ecef = np.reshape(nadir_ecef, (3, 1))

    # check if all vectors have same size
    if np.logical_or(np.size(inclination_angle) != np.size(nadir_ecef, 1),
                     np.size(inclination_angle) != np.size(flag_asc_desc)):
        raise NameError('parameters do not have all the same size')

    # <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

    # first define 90 deg inclination.
    vect = np.zeros((3, np.size(inclination_angle)))
    vect[:, flag_asc_desc == 'ASC'] = np.array([-nadir_ecef[1], nadir_ecef[0], np.zeros_like(nadir_ecef[0])])[:,
                                      flag_asc_desc == 'ASC']
    vect[:, flag_asc_desc == 'DESC'] = np.array([nadir_ecef[1], -nadir_ecef[0], np.zeros_like(nadir_ecef[0])])[:,
                                       flag_asc_desc == 'DESC']

    # normalize
    norm_vect = np.sum(vect * vect, axis=0) ** 0.5

    #    vect_result = np.atleast_2d(vect/norm_vect).T
    vect_result = (vect / norm_vect).reshape((3, np.size(vect) / 3))

    # then perform rotation on Z-axis
    # TODO : vectorize to enhance speed !
    norm_nadir_ecef = np.sum(nadir_ecef * nadir_ecef, axis=0) ** 0.5
    nadir_ecef_unit = nadir_ecef / norm_nadir_ecef

    counter = 0
    inclination_angle = inclination_angle - np.pi / 2

    for inc in inclination_angle:
        ux = np.atleast_2d(nadir_ecef_unit).reshape((3, np.size(nadir_ecef_unit) / 3))[0, counter]
        uy = np.atleast_2d(nadir_ecef_unit).reshape((3, np.size(nadir_ecef_unit) / 3))[1, counter]
        uz = np.atleast_2d(nadir_ecef_unit).reshape((3, np.size(nadir_ecef_unit) / 3))[2, counter]

        mat_rotation = np.array([[np.cos(inc) + ux ** 2 * (1 - np.cos(inc)),
                                  ux * uy * (1 - np.cos(inc)) - uz * np.sin(inc),
                                  ux * uz * (1 - np.cos(inc)) + uy * np.sin(inc)], \
                                 [ux * uy * (1 - np.cos(inc)) + uz * np.sin(inc),
                                  np.cos(inc) + uy ** 2 * (1 - np.cos(inc)),
                                  uy * uz * (1 - np.cos(inc)) - ux * np.sin(inc)], \
                                 [ux * uz * (1 - np.cos(inc)) - uy * np.sin(inc),
                                  uy * uz * (1 - np.cos(inc)) + ux * np.sin(inc),
                                  np.cos(inc) + uz ** 2 * (1 - np.cos(inc))]])

        vect_result[:, counter] = np.dot(mat_rotation, vect_result[:, counter])

        counter += 1


    #       #TODO : clean reshaped stuff
    # if vector is 1D then output must 1D as well
    if flag_output_1D:
        vect_result = vect_result.reshape((3,))

    return vect_result


# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def compute_ecef_2_sc_rot_matrix(nadir, sat_pos, normal_vector):
    ''' This function compute the vectors, in ECEF,  of the spacecraft coordinate system, for X satellites
    This is used to derive matrices to switch from (ecef) to (sc) coordinates system
    Note : can be used "vector-like" to compute matrices for several satellites at a time
    Input  : 
        - nadir : [3,X] array of nadir positions (e.g. in ECEF) in kms
        - sat_pos : [3,X] array of satellite positions (e.g. in ECEF) in kms
        - normal_vector : [3,X] vectors normal to the orbital plan of each satellite
    
    Output : 
        - set of matrices from (ecef) to (sc). Output has the form [3,3,X]
    
    '''

    z = nadir - sat_pos
    z = z / np.sum(z * z, axis=0) ** 0.5

    y = normal_vector
    y = y / np.sum(y * y, axis=0) ** 0.5

    x = np.cross(y, z, axis=0)
    x = x / np.sum(x * x, axis=0) ** 0.5

    return np.array([x, y, z])  # return les 3 vecteurs normalisés, qui
    # forment aussi la matrice de passage de ECEF vers SC
    # TODO : make sure form is [3,3,X]


# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def compute_xyz_rot_matrices(x_angle, y_angle, z_angle):
    ''' This function computes the x_angle, y_angle, z_angle, rotation matrix, for X satellites simultaneously
    
    Input :
        - x_angle  : [X] vector or x_angle angles in radian
        - y_angle : [X] vector or y_angle angles in radian
        - z_angle   : [X] vector or z_angle angles in radian
        
    Output :
        - [3,3,X] array representing the X (3,3) matrices of rotation (one per satellite)
    
    
    '''

    first_col = np.array([np.cos(z_angle) * np.cos(y_angle),
                          np.cos(z_angle) * np.sin(y_angle) * np.sin(x_angle) - np.sin(z_angle) * np.cos(x_angle),
                          np.cos(z_angle) * np.sin(y_angle) * np.cos(x_angle) + np.sin(z_angle) * np.sin(x_angle)])

    second_col = np.array([np.sin(z_angle) * np.cos(y_angle),
                           np.sin(z_angle) * np.cos(y_angle) * np.sin(x_angle) + np.cos(z_angle) * np.cos(x_angle),
                           np.sin(z_angle) * np.sin(y_angle) * np.cos(x_angle) - np.cos(z_angle) * np.sin(x_angle)])

    third_col = np.array([-np.sin(y_angle), np.cos(y_angle) * np.sin(x_angle), np.cos(y_angle) * np.cos(x_angle)])

    rotation_mat = np.array([first_col, second_col, third_col])

    return rotation_mat


# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
def multi_matrix_product(rot_mat, points_to_rotate):
    '''
    This function applies one or many rotation matrices onto points to rotate
    (simple numpy matrix product cannot be directly applied)
    description to be enhanced
    '''

    points_rotated = np.einsum('ij...,j...', rot_mat, points_to_rotate).T

    # <><><><><><> Consistency <><><><><><><>
    #    if points_to_rotate.ndim == 1:
    #        points_rotated = np.reshape(points_rotated, (3))
    # <><><><><><> Consistency <><><><><><><>

    return points_rotated


#    # case with 1D vectors
#    if sat_pos_ecef.ndim == 1:
#        points_sat_coord = np.dot(mat_ecef2sat, (vect_ecef.T - sat_pos_ecef.T).T) #TODO : change the ugly tranpose (
# this is to handle 1D vectors)
#
#        
#    else:
#    
#        # matrix calculation using np.einsum
#        #( replaces code found on Internet :
# https://jameshensman.wordpress.com/2010/06/14/multiple-matrix-multiplication-in-numpy/)
#         vect_to_mult = (vect_ecef.T - sat_pos_ecef.T).T #TODO : change the ugly tranpose
#         points_sat_coord = np.einsum('ij...,j...',mat_ecef2sat,vect_to_mult).T       


# -----------------------------------------------------------------------------



# ----------------------------------------------------------------------------
def compute_intersection_WGS84_ecef(vectors, sat_pos):
    """ computes intersection of a line (defined by directing vector in ECEF coord. system, starting from a satellite)
    with the WGS84 ellipsoid
    Note : This is for X lines with X satellites, but works also if only one satellite is used (broadcasting)
    
    Input : 
        - vectors : [3,X] array of (x,y,z)ecef vectors (e.g. unitary vectors)
        - sat_pos : [3,X] array of (x,y,z)ecef satellite positions in kms
    
    Output :
        - [3,X] array of (x,y,z)ecef points on WGS 84 ellipsoid in kms
    """

    RTE_2 = 6378.1370 ** 2  # % equatorial radius RTE (km)
    RTP_2 = 6356.7523 ** 2  # % pole radius RTP (km)

    # Intersection between line and ellipsoide consists in solving a 2nd degree equation

    A = (vectors[0] ** 2 + vectors[1] ** 2) / RTE_2 + vectors[2] ** 2 / RTP_2

    B = 2 * ((vectors[0] * sat_pos[0] + vectors[1] * sat_pos[1]) / RTE_2 + vectors[2] * sat_pos[2] / RTP_2)

    C = (
    (sat_pos[0] ** 2 + sat_pos[1] ** 2) / RTE_2 + sat_pos[2] ** 2 / RTP_2 - 1)  # *np.ones((np.size(ecef_points,0),1))

    delta = B ** 2 - 4 * A * C

    result = (-B - np.sqrt(delta)) / (2 * A)

    return np.array(
        [vectors[0] * result + sat_pos[0], vectors[1] * result + sat_pos[1], vectors[2] * result + sat_pos[2]])


# ----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
def compute_uvw_sc_nominal_2_unitary_ecef(vect_sat, nadir_ecef, sat_pos_ecef, normal_vector):
    '''
    Description TODO: switch from SC nominal to unitary ECEF
    
    '''
    # TODO : perform the checks

    # compute matrix to go to SC coord. system
    # TODO : create optional parameter for matrix (if has been computed already)
    mat_ecef2sat = compute_ecef_2_sc_rot_matrix(nadir_ecef, sat_pos_ecef,
                                                normal_vector)  # rotation matrix to go to SAT coordinate system

    if np.ndim(mat_ecef2sat) == 3:
        mat_sat_2_ecef = np.transpose(mat_ecef2sat, (1, 0, 2))
    else:
        mat_sat_2_ecef = np.transpose(mat_ecef2sat)

    return multi_matrix_product(mat_sat_2_ecef, vect_sat)

#    # case with 1D vectors
#    if sat_pos_ecef.ndim == 1:
#        points_ecef = np.dot(mat_sat.transpose(), vect_sat)
#        
#
#        
#    else:
#    
#        # matrix calculation (smartly done with code found on Internet :
# https://jameshensman.wordpress.com/2010/06/14/multiple-matrix-multiplication-in-numpy/)
#
#        # transpose matrix
#    
#        mat_sat_transposed = np.transpose(mat_sat, (1, 0, 2))
#        # vect_to_mult = vect_ecef - sat_pos_ecef
#        points_ecef = np.einsum('ij...,j...', mat_sat_transposed, vect_sat).T       


#    return points_ecef
# -----------------------------------------------------------------------------
