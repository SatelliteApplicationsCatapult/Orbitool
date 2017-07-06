# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 09:12:39 2014

***REMOVED***


MODULE
"""

import os
import subprocess
from scipy.special import j1

from lbConfiguration import pathtopropa
from .geometric_func import *
from .ant_func import *

k_dB = -228.6  # Boltzmann's constant

# ________________________________________________________________________________________
#########################################################################################
# UTILITIES, DISTANCE AND RF PERFOS CALCULATIONS
# ________________________________________________________________________________________
#########################################################################################


# _----------------------------------------------------------------------------------------
def compute_elev_grd_wrap(lon, lat, sat_pos_x, sat_pos_y, sat_pos_z):
    '''
	This functions only wraps the compute_elev_grd function in the geometric_func library, in order to create a
	(potential) array of satellite positions out of their X,Y,Z coordinates (if there is only one satellite it creates a 3D vector)
	NOTE : sat_pos can be either one satellite (use broadcasting of numpy) or an array of satellite positions
    equaling the size of (lon,lat) couples
	'''
    sat_pos = np.array([sat_pos_x, sat_pos_y, sat_pos_z])
    pos_station = ll_geod2ecef(np.array([lon, lat]))

    return compute_elev_grd(pos_station, sat_pos)


# _----------------------------------------------------------------------------------------



# _----------------------------------------------------------------------------------------
def db_join(target_dict, data_dict, field_to_add, key_list, default_value='none'):
    '''

    This function is a utility that is used to perform a "join" operation (similar as SQL) between two different data dictionnaries.
    Note that a "data dictionnary" in this SW is expected to have Numpy [1,X] arrays as elements.
    Both dictionnaries must have a column (or a set of columns) in common, that has the same name, to perform the joining operation.

    Example : SAT dict has columns "SAT_ID" and "SIZE"
              EARTH_COORD_VSAT dict has columns "SAT_ID" and "LON/LAT"
              db_join(EARTH_COORD_VSAT, SAT, "SIZE", "SAT_ID") will output a vector representing for point in EARTH_COORD_VSAT dict the satellite SIZE associated.
    Please look into SQL join on Internet to get a better understanding of the function.

    Input :
        - target_dict : Python dictionnary on which the join will be performed
        - data_dict : Python dictionnary on which the data will be used to perform the join
        - field to add : String representing the data we want to add to the target_dict
        - key_list : String or String list representing the column(s) to be used as key for the join

    Output :
        - a [X] vector, of the size of an element of the target_dict


    '''
    # check dtype of data

    data_dtype = data_dict[field_to_add].dtype

    # check if list (otherwise means only one value)
    if not (type(key_list) is list):
        key_list = [key_list]

    # create empty entry in dict
    # assumption: considered columns of target dict (keys + field to add) are the same size
    # TODO : check consistency (if not all values are assigned)
    if default_value == 'none':
        vect_res = np.empty_like(target_dict[key_list[0]], dtype=data_dtype)
    else:
        vect_res = np.ones_like(target_dict[key_list[0]], dtype=data_dtype) * default_value

    for i in np.arange(0, np.size(data_dict[key_list[0]])):
        #        mask_useful_values = np.ones_like(target_dict[key_list[0]]).astype(bool)
        mask_useful_values = target_dict[key_list[0]] == data_dict[key_list[0]][i]
        for j in np.arange(1, len(key_list)):
            mask_useful_values = np.logical_and(mask_useful_values,
                                                target_dict[key_list[j]] == data_dict[key_list[j]][i])
        vect_res[mask_useful_values] = data_dict[field_to_add][i]

    return vect_res


# _----------------------------------------------------------------------------------------

# _----------------------------------------------------------------------------------------
def db_join_old(target_dict, data_dict, field_to_add, key):
    '''
    DEPRECATED
    '''

    # check dtype of data
    data_dtype = data_dict[field_to_add].dtype

    # create empty entry in dict
    # assumption: all columns of target dict are the same size
    target_dict[field_to_add] = np.empty_like(target_dict[target_dict.keys()[0]], dtype=data_dtype)

    # then perform join operation
    ctr = 0
    for item in data_dict[key]:
        target_dict[field_to_add][target_dict[key] == item] = data_dict[field_to_add][ctr]

        ctr += 1

    return target_dict


# _----------------------------------------------------------------------------------------

# _----------------------------------------------------------------------------------------
def compute_distance_to_sat(grd_pos_x, grd_pos_y, grd_pos_z, sat_pos_x, sat_pos_y, sat_pos_z):
    '''
    Computes distance between points on Earth (grd_pos_..) and their associated satellites (sat_pos_..)

    Inputs :
     - grd_pos_x : [X] array of X coordinate of ground stations, in ECEF and in kms
     - grd_pos_y : [X] array of Y coordinate of ground stations, in ECEF and in kms
     - grd_pos_z : [X] array of Z coordinate of ground stations, in ECEF and in kms
     - sat_pos_x : [X] array of X coordinate of ground stations, in ECEF and in kms (can also be a scalar : see NOTE below)
     - sat_pos_y : [X] array of Y coordinate of ground stations, in ECEF and in kms (can also be a scalar : see NOTE below)
     - sat_pos_z : [X] array of Z coordinate of ground stations, in ECEF and in kms (can also be a scalar : see NOTE below)

    Output :
    - [X] vector of distances between ground stations and their associated satellites

    NOTE : sat_pos can alternately be only one satellite (meaning that distance computed for each ground station is the one related to that particular
    satellite) or an array of satellite positions equaling the size of the number of ground stations (meaning each ground station is affected a particular
    satellite that can be different for each ground station)
    '''

    sat_pos = np.array([sat_pos_x, sat_pos_y, sat_pos_z])
    vect_dist = np.array([grd_pos_x, grd_pos_y, grd_pos_z]) - sat_pos
    #    vect_dist = ll_geod2ecef(np.array([lon,lat])) - sat_pos

    return np.sum(vect_dist * vect_dist, axis=0) ** 0.5;  # in m


# _----------------------------------------------------------------------------------------


# _----------------------------------------------------------------------------------------
def compute_fsl(distance, freq):
    ''' Computes Free Space Loss attenuation
	Inputs :
         - distance :  [X] vector of distances
	   - freq        [X] vector of frequencies (can also be a scalar of one frequency only : see NOTE below)

     Outputs :
         - [X] vector of FSLs


    NOTE : freq can alternately be one frequency (in which case FSL is computed with respect to that particular frequency) or
    a vector with as many elements as the "distance" vector, in case one would like to specify different frequencies for each element

     '''
    # compute FREE SPACE LOSSES
    # distance in kilometers
    # freq in MHz
    # note : works with vectors as inputs
    fsl_lin = (4 * np.pi * distance * 1e3 * freq * 1e6 / 3e8) ** 2

    return 10 * np.log10(fsl_lin)

#
# # _----------------------------------------------------------------------------------------
#
#
# # _----------------------------------------------------------------------------------------
# def compute_propag(lon, lat, alt, elevation, freq, tilt_polar_angle, diameter, efficiency, availability):
#     '''
#     This function computes propagation attenuation due to rain conditions, using the CNES library available at :
#
#     description : TODO
#     '''
#
#     #    # compute propagation losses
#     #    # freq in MHz
#     #    # availability in percentage (%)
#     #    #vectorized
#     #
#     #    # convert freq in GHz
#     #    freq = freq /1e3
#     #
#     #    # convert elevation in radians
#     #    elevation = elevation * np.pi/180
#     #
#     #    # compute "percentage of time"
#     #    time_pct = 100 - availability*100
#     #
#     #    # initiate values
#     #    vct = np.arange(0,np.size(lon),1)
#     #    Agaseous = np.zeros(np.size(lon))
#     #    Aclouds = np.zeros(np.size(lon))
#     #    Iscint = np.zeros(np.size(lon))
#     #    Arain = np.zeros(np.size(lon))
#     #
#     #
#     #    for ctr in vct:
#     #
#     #        # Intermediate parameters computation
#     #        hr = rain_height(lat[ctr],lon[ctr])
#     #        R001 = rain_intensity(lat[ctr],lon[ctr],0.01)
#     #        Temp = temperature(lat[ctr],lon[ctr])
#     #        ro = SWVD(lat[ctr],lon[ctr])
#     ##        WVC = IWVC(lat[ctr],lon[ctr],time_pct[ctr])
#     #        LWC = LWCC(lat[ctr],lon[ctr],time_pct[ctr])
#     #        Nwet = NWET(lat[ctr],lon[ctr])
#     #
#     #
#     #        # GASEOUS ATTENUATION
#     #        Agaseous[ctr] = gaseous_attenuation(freq[ctr],elevation[ctr],Temp,ro);
#     #
#     #        # GASEOUS ATTENUATION EXCEEDED FOR availability% OF THE TIME
#     ##        Agaseous = gaseous_attenuation_exc(freq[ctr],elevation[ctr],Temp,WVC,ro)
#     #
#     #        # CLOUD ATTENUATION EXCEEDED FOR availability% OF THE TIME
#     #        Aclouds[ctr] = cloud_attenuation(freq[ctr],elevation[ctr],LWC)
#     #
#     #        # IMPAIRMENT DUE to SCINTILLATION EXCEEDED FOR availability% OF THE TIME
#     #        Iscint[ctr] = scintillation(Nwet,freq[ctr],elevation[ctr],time_pct[ctr],alt[ctr],efficiency[ctr],diameter[ctr])
#     #
#     #        # RAIN ATTENUATION EXCEEDED FOR availability% OF THE TIME
#     #        Arain[ctr] = rain_attenuation(lat[ctr],freq[ctr],elevation[ctr],time_pct[ctr],alt[ctr],hr,R001,tilt_polar_angle[ctr])
#     #
#     #    # A TOTAL
#     #    Atot = Agaseous + np.sqrt((Aclouds + Arain)**2 + Iscint**2)
#
#     # for the moment : bypass function (wait fro CNES library update)
#     Atot = np.zeros_like(lon)
#
#     return Atot


# _----------------------------------------------------------------------------------------


# _----------------------------------------------------------------------------------------
def compute_polar_tilt_angle(polar_array):
    ''' Compute polarization tilt angle (done only for circular at the moment)
    Input :  [X] vector-like array of char
    Output : [X] vector of polar tilt angles
    '''

    tilt_angle = np.zeros_like(polar_array, dtype='float64')

    # Tilt angle for circular polarization
    tilt_angle[polar_array == 'C'] = 45

    return tilt_angle


# TODO : handle vertical and horizontal

# _----------------------------------------------------------------------------------------


# _----------------------------------------------------------------------------------------
# def assign_transponder(lon, lat, sat_pos_ecef, nadir_ecef, sat_id, flag_orbit, trsp_az_ant, trsp_el_ant, trsp_id):
def assign_transponder(lon, lat, sat_pos_ecef, nadir_ecef, normal_vector, sat_id, trsp_az_ant, trsp_el_ant, trsp_id):
    '''
    DEPRECATED / NOT USED ANYMORE AT THE MOMENT

    This function assign every point of a coverage to a transponder.
    It does it at the moment by comparing distance in lon,lat to transponder center
    Note : this is very wrong in the general case but sufficient for constellation analysis
    '''

    # TODO : change function to base it on gain
    # should be several options :
    # one is compare to closeness to antenna target center

    # compute propagation losses
    # freq in MHz
    # availability in percentage (%)


    # loop over satellites
    dist_sq = 720 ** 2 * np.ones_like(lon)
    indices_sat = np.zeros_like(lon)
    indices_trsp = np.zeros_like(lon)
    counter_sat = 0

    for i in np.arange(0, np.size(nadir_ecef) / 3):

        nadir = nadir_ecef[:, i]
        sat_pos = sat_pos_ecef[:, i]
        normal_vect = normal_vector[:, i]
        # TODO : change nadir and sat_pos
        counter_trsp = 0

        for az_elev in np.array([trsp_az_ant, trsp_el_ant]).transpose():
            # convert into lon_lat
            points_ecef = compute_az_elev_to_ecef(az_elev, \
                                                  nadir, \
                                                  sat_pos, \
                                                  normal_vect \
                                                  )
            lonlat = ecef2ll_geod(points_ecef)

            # find who is closest
            angle_min_lon = np.minimum(lonlat[0] - lon, lonlat[0] + 360 - lon)
            angle_min_lat = np.minimum(lonlat[1] - lat, lonlat[1] + 180 - lat)
            new_dist_sq = np.sum(np.array([angle_min_lon, angle_min_lat]) ** 2, axis=0)
            #           new_dist_sq4 =  np.sum(np.array([lonlat[0]- lon,lonlat[1]- lat])**2,axis = 0)
            mask_min = new_dist_sq <= dist_sq
            indices_sat[mask_min] = counter_sat
            indices_trsp[mask_min] = counter_trsp
            dist_sq[mask_min] = new_dist_sq[mask_min]
            counter_trsp += 1
        counter_sat += 1

    # TODO : check compat entre indices sat et TRSP_ID
    return sat_id[indices_sat.astype(np.int16)], trsp_id[indices_trsp.astype(np.int16)]  # dBs


# _----------------------------------------------------------------------------------------


# _----------------------------------------------------------------------------------------
# def assign_transponder(lon, lat, sat_pos_ecef, nadir_ecef, sat_id, flag_orbit, trsp_az_ant, trsp_el_ant, trsp_id):
def assign_transponder2(grd_points_ecef, sat_pos_ecef, sat_id, trsp_az_ant=np.array([0.0]), trsp_el_ant=np.array([0.0]),
                        trsp_id=np.array([])):
    '''
    DEPRECATED / NOT USED ANYMORE AT THE MOMENT

    This function assign every point of a coverage to a transponder.
    It does it at the moment by comparing elevation of station to transponder center
    '''

    # TODO : change function to base it on gain
    # should be several options :
    # one is compare to closeness to antenna target center


    elevations = np.zeros(np.size(grd_points_ecef) / 3) * 0.0
    indices_sat = np.zeros(np.size(grd_points_ecef) / 3)
    indices_trsp = np.zeros(np.size(grd_points_ecef) / 3)
    counter_sat = 0

    # case if only one satellite
    if sat_pos_ecef.ndim == 1:
        sat_pos_ecef = np.reshape(sat_pos_ecef, (3, 1))

        # loop over satellites
    for i in np.arange(0, np.size(sat_pos_ecef) / 3):

        # TODO : act special if sat_pos_ecef is not 2D
        sat_pos = sat_pos_ecef[:, i]  # TODO : change sat_pos ?
        counter_trsp = 0

        # loop over transponder of same satellite
        for az_elev in np.array([trsp_az_ant, trsp_el_ant]).transpose():
            # compute elevation of each point
            new_elev = compute_elev_grd(grd_points_ecef, sat_pos)

            mask_better_elevs = new_elev > elevations
            indices_sat[mask_better_elevs] = counter_sat
            indices_trsp[mask_better_elevs] = counter_trsp
            elevations[mask_better_elevs] = new_elev[mask_better_elevs]
            counter_trsp += 1
        counter_sat += 1

    # TODO : check compat entre indices sat et TRSP_ID
    return sat_id[indices_sat.astype(np.int16)], trsp_id[indices_trsp.astype(np.int16)], elevations  # dBs


# _----------------------------------------------------------------------------------------

# _----------------------------------------------------------------------------------------
def assign_transponder3(grd_points_ecef, sat_pos_ecef, nadir_ecef, normal_vector, sat_id, \
                        sat_pl_id=np.array([]), trsp_az_ant=np.array([0.0]), trsp_el_ant=np.array([0.0]),
                        trsp_id=np.array([0]), trsp_pl_id=np.array([])):
    '''
    This function assigns every point of a coverage to a transponder.
    It does it at the moment by comparing semi angle of satellite transponder aperture
    '''

    # TODO : change function to base it on gain
    # TODO : add roll, pitch, yaw onto function
    # should be several options :
    # one is compare to closeness to antenna target center


    theta_ant = np.ones(np.size(grd_points_ecef) / 3) * 90.0
    indices_sat = np.zeros(np.size(grd_points_ecef) / 3)
    indices_trsp = np.zeros(np.size(grd_points_ecef) / 3)
    counter_sat = 0

    # case if only one satellite
    if sat_pos_ecef.ndim == 1:
        sat_pos_ecef = np.reshape(sat_pos_ecef, (3, 1))

        # loop over satellites
    for i in np.arange(0, np.size(sat_pos_ecef) / 3):

        # TODO : act special if sat_pos_ecef is not 2D
        sat_pos = sat_pos_ecef[:, i]  # TODO : change sat_pos ?
        nadir = nadir_ecef[:, i]
        normal_vect = normal_vector[:, i]
        counter_trsp = 0

        # compute elevation of each point : mandatory
        elev = compute_elev_grd(grd_points_ecef,
                                sat_pos)  # TODO : this function does not take into account R,P,Y, or X,Y,Z antenna coord. system
        mask_elev = elev > 30  # TODO : change this elevation threshold

        if np.sum(mask_elev) > 0:
            # compute semi_angle of grd points
            #            az_elev_sat = compute_ecef_to_az_elev(grd_points_ecef[:,mask_elev], \
            #                                nadir, \
            #                                sat_pos, \
            #                                normal_vect \
            #                                ) # TODO : here add R,P,Y


            points_sat_coord = compute_ecef_2_sc_nominal(grd_points_ecef[:, mask_elev], nadir, sat_pos, normal_vect)

            #    Perform roll,pitch, yaw rotation IF any is specified
            #            if np.any(np.isnan(roll)):
            #                points_sat_coord_tilted = points_sat_coord
            #            else:
            #                points_sat_coord_tilted = compute_coord_system_rotation(points_sat_coord, roll, pitch, yaw)
            #
            #            #   Perform rotation to go to Antenna Coordinate System IF any is specified (otherwise it is considered that antenna coord. system is the same as the satellite one)
            #            if np.any(np.isnan(Rx)):
            #                points_ant_coord = points_sat_coord_tilted
            #            else:
            #                points_ant_coord = compute_coord_system_rotation(points_sat_coord_tilted, Rx, Ry, Rz)

            # Azimuth, elevation of points
            az_elev_sat = compute_sat_2_ab(points_sat_coord)

            # loop over transponder of same satellite
            if np.size(trsp_pl_id) > 0:
                mask_trsp = (trsp_pl_id == sat_pl_id[i])
            else:
                mask_trsp = np.bool(1)

            # TODO : here we don't need az elev of beam centers
            trsp_az_ant_to_consider = trsp_az_ant[mask_trsp]
            trsp_elev_ant_to_consider = trsp_el_ant[mask_trsp]
            index_useful_trsp = np.nonzero(mask_trsp)[0]

            for az_elev_trsp in np.array([trsp_az_ant_to_consider, trsp_elev_ant_to_consider]).transpose():
                # compute semi_angle transponder
                # TODO : use adequate function instead ? (translate_az_elev_sc_to_az_elev_ant)
                # TODO : change by computing X,Y,Z and then az,elev
                az_elev_ant = (az_elev_sat.T - az_elev_trsp).T

                new_theta_ant = np.sum(az_elev_ant ** 2, axis=0) ** 0.5

                mask_better_theta = new_theta_ant < theta_ant[mask_elev]

                # update vector of best thetas, and indices
                values_indices_sat = indices_sat[mask_elev]
                values_indices_trsp = indices_trsp[mask_elev]
                values_theta = theta_ant[mask_elev]

                values_indices_sat[mask_better_theta] = counter_sat
                values_indices_trsp[mask_better_theta] = index_useful_trsp[counter_trsp]
                values_theta[mask_better_theta] = new_theta_ant[mask_better_theta]

                indices_sat[mask_elev] = values_indices_sat
                indices_trsp[mask_elev] = values_indices_trsp
                theta_ant[mask_elev] = values_theta
                #                theta_ant[mask_elev][mask_better_theta] = new_theta_ant[mask_better_theta]
                counter_trsp += 1
        counter_sat += 1

    # TODO : check compat entre indices sat et TRSP_ID
    return sat_id[indices_sat.astype(np.int16)], trsp_id[indices_trsp.astype(np.int16)]  # dBs


# -----------------------------------------------------------------------------------------


# _----------------------------------------------------------------------------------------
def assign_transponder_test(grd_points_ecef, \
                            sat_pos_ecef, \
                            nadir_ecef, \
                            normal_vector, \
                            sat_id, \
                            sat_roll=np.nan, \
                            sat_pich=np.nan, \
                            sat_yaw=np.nan, \
                            sat_pl_id=np.array([]), \
                            trsp_x_angle=np.array([0.0]), \
                            trsp_y_angle=np.array([0.0]), \
                            trsp_z_angle=np.array([0.0]), \
                            trsp_id=np.array([0]), \
                            trsp_pl_id=np.array([])):
    '''
    This function assigns every point of a coverage to a transponder.
    It does it at the moment by comparing semi angle of satellite transponder aperture
    '''

    # TODO : change function to base it on gain
    # TODO : add roll, pitch, yaw onto function
    # should be several options :
    # one is compare to closeness to antenna target center


    theta_ant = np.ones(np.size(grd_points_ecef) / 3) * 90.0
    indices_sat = np.zeros(np.size(grd_points_ecef) / 3)
    indices_trsp = np.zeros(np.size(grd_points_ecef) / 3)
    counter_sat = 0

    # case if only one satellite
    if sat_pos_ecef.ndim == 1:
        sat_pos_ecef = np.reshape(sat_pos_ecef, (3, 1))

        # loop over satellites
    for i in np.arange(0, np.size(sat_pos_ecef) / 3):

        # TODO : act special if sat_pos_ecef is not 2D
        sat_pos = sat_pos_ecef[:, i]  # TODO : change sat_pos ?
        nadir = nadir_ecef[:, i]
        normal_vect = normal_vector[:, i]
        roll = sat_roll[:, i]
        pitch = sat_pitch[:, i]
        yaw = sat_yaw[:, i]
        counter_trsp = 0

        # compute elevation of each point : mandatory
        elev = compute_elev_grd(grd_points_ecef,
                                sat_pos)  # TODO : this function does not take into account R,P,Y, or X,Y,Z antenna coord. system
        mask_elev = elev > 30  # TODO : change this elevation threshold

        if np.sum(mask_elev) > 0:
            # compute semi_angle of grd points
            # TODO : stop at roll pitch yaw, 3D vector
            #            az_elev_sat = compute_ecef_to_az_elev(grd_points_ecef[:,mask_elev], \
            #                                nadir, \
            #                                sat_pos, \
            #                                normal_vect \
            #                                ) # TODO : here add R,P,Y
            points_sat_coord = compute_ecef_2_sc_nominal(grd_points_ecef[:, mask_elev], nadir_ecef, sat_pos_ecef,
                                                         normal_vector)
            #            Perform roll,pitch, yaw rotation IF any is specified
            if np.any(np.isnan(roll)):
                points_sat_coord_tilted = points_sat_coord
            else:
                points_sat_coord_tilted = compute_coord_system_rotation(points_sat_coord, roll, pitch, yaw)

            # loop over transponder of same satellite
            if np.size(trsp_pl_id) > 0:
                mask_trsp = (trsp_pl_id == sat_pl_id[i])
            else:
                mask_trsp = np.bool(1)

            # TODO : here we don't need az elev of beam centers, but XYZ params
            trsp_x_angle_to_consider = trsp_x_angle[mask_trsp]
            trsp_y_angle_to_consider = trsp_y_angle[mask_trsp]
            trsp_z_angle_to_consider = trsp_z_angle[mask_trsp]
            #            trsp_az_ant_to_consider =  trsp_az_ant[mask_trsp]
            #            trsp_elev_ant_to_consider =  trsp_el_ant[mask_trsp]
            index_useful_trsp = np.nonzero(mask_trsp)[0]

            for Rxyz in np.array(
                    [trsp_x_angle_to_consider, trsp_y_angle_to_consider, trsp_z_angle_to_consider]).transpose():

                # compute semi_angle transponder
                # TODO : use adequate function instead ? (translate_az_elev_sc_to_az_elev_ant)
                # TODO : change by computing X,Y,Z and then az,elev
                #   Perform rotation to go to Antenna Coordinate System IF any is specified (otherwise it is considered that antenna coord. system is the same as the satellite one)
                if np.sum(np.abs(np.Rxyz)) == 0:
                    points_ant_coord = points_sat_coord_tilted
                else:
                    points_ant_coord = compute_coord_system_rotation(points_sat_coord_tilted, Rxyz[0], Rxyz[1], Rxyz[2])

                az_elev = compute_az_elev(points_ant_coord)

                #                az_elev_ant = (az_elev_sat.T - az_elev_trsp).T

                #                new_theta_ant = np.sum(az_elev_ant**2,axis=0)**0.5
                new_theta_ant = az_elev[:, 1]

                mask_better_theta = new_theta_ant < theta_ant[mask_elev]

                # update vector of best thetas, and indices
                # TODO refine this and in particular check payload ID
                values_indices_sat = indices_sat[mask_elev]
                values_indices_trsp = indices_trsp[mask_elev]
                values_theta = theta_ant[mask_elev]

                values_indices_sat[mask_better_theta] = counter_sat
                values_indices_trsp[mask_better_theta] = index_useful_trsp[counter_trsp]
                values_theta[mask_better_theta] = new_theta_ant[mask_better_theta]

                indices_sat[mask_elev] = values_indices_sat
                indices_trsp[mask_elev] = values_indices_trsp
                theta_ant[mask_elev] = values_theta
                #                theta_ant[mask_elev][mask_better_theta] = new_theta_ant[mask_better_theta]
                counter_trsp += 1
        counter_sat += 1

    # TODO : check compat entre indices sat et TRSP_ID
    return sat_id[indices_sat.astype(np.int16)], trsp_id[indices_trsp.astype(np.int16)]  # dBs


# -----------------------------------------------------------------------------------------






# __________________________________________________________________________________________________
###################################################################################################
#                     LINK BUDGET FUNCTIONS
# __________________________________________________________________________________________________
###################################################################################################




####################################################################################################
def compute_OBO(ibo):
    ''' This function returns the OBO of a transponder, provided the IBO and the AM/AM curve of the amplifier'''
    #    TODO : replace with real function interpolating an AM/AM curve
    return 3 * np.ones_like(ibo)


####################################################################################################



####################################################################################################
def compute_EIRP(amp_sat, obo, sat_gain_tx):
    ''' this function computes the EIRP of an emitter
    amp_sat is amplification at saturation in Watts
    obo and tx gain are in dB already'''

    return 10 * np.log10(amp_sat) - obo + sat_gain_tx


####################################################################################################


####################################################################################################
def compute_CSN0_DN(eirp, fsl_dn, propag_dn, gpt):
    ''' compute C/N0 downlink. assumes sat eirp has been already calculated '''
    return eirp - fsl_dn - propag_dn + gpt - k_dB


####################################################################################################

####################################################################################################
def compute_CSN0_UP(eirp_grd, fsl_up, propag_up, gpt_sat):
    ''' compute C/N0 downlink. assumes ground eirp has been already calculated '''
    return eirp_grd - fsl_up - propag_up + gpt_sat - k_dB


####################################################################################################

####################################################################################################
def compute_csn0_total(csn0_up, csi0_up, csim0, csn0_dn, csi0_dn):
    return -10 * np.log10(10 ** (-csn0_up / 10) + \
                          10 ** (-csi0_up / 10) + \
                          10 ** (-csim0 / 10) + \
                          10 ** (-csn0_dn / 10) + \
                          10 ** (-csi0_dn / 10))


####################################################################################################

####################################################################################################
def compute_csn_fwd(csn0, bandwidth):
    ''' computes C/N in the FORWARD LINK ONLY !!! '''
    return csn0 - 10 * np.log10(bandwidth * 1e6)


####################################################################################################

####################################################################################################
def compute_eff_spec(csn, flag_waveform):
    ''' computes spectral efficiency, depending on waveform (only Shannon theo. implemented yet) '''
    if (flag_waveform == 'shannon'):
        return np.log2(1 + 10 ** (csn / 10))
    elif (flag_waveform == 'DVB-S2'):
        dvb_s2 = np.array([[0.357, -1.50], \
                           [0.616, -0.30], \
                           [0.745, 0.60], \
                           [0.831, 1.90], \
                           [1.132, 3.10], \
                           [1.261, 4.00], \
                           [1.390, 4.90], \
                           [1.476, 5.60], \
                           [1.562, 6.10], \
                           [1.691, 7.10], \
                           [1.885, 7.80], \
                           [2.078, 9.10], \
                           [2.335, 10.50], \
                           [2.762, 11.50], \
                           [2.933, 12.30], \
                           [3.104, 12.90]])
        # look for index of closest value
        indices_values = np.searchsorted(dvb_s2[:, 1], csn)
        values = dvb_s2[indices_values - 1, 0]

        # special treatment for values out of the array (left side)
        values[csn < dvb_s2[0, 1]] = 0
        return values


    else:
        return 0


####################################################################################################

####################################################################################################
def compute_capacity(earth_coord_trsp_id, earth_coord_sat_id, earth_coord_rs, earth_coord_eff_spec, flag_fwd_rtn):
    '''

    what is done at the moment : compute capacity of each terminal, with fixed Rs to everyone

    options that should exist :
        - depending on frequency allocation (fixed Rs to everyone, or fixed capacity to everyone, or weighted with user needs)
    '''

    capa_ratio = np.ones_like(earth_coord_trsp_id)

    list_trsp_ids = np.unique(earth_coord_trsp_id)
    list_sat_ids = np.unique(earth_coord_sat_id)

    if flag_fwd_rtn == 'FWD':
        # find out all points in the same beam, and divide the allocated frequency between them
        # Option 1 : each point gets the same amount of frequency
        for sat_id in list_sat_ids:
            #        payload_id = earth_coord_payload_id[earth_coord_sat_id == sat_id][0] #assumption : one satellite can only have one payload id

            for trsp_id in list_trsp_ids:
                points_trsp = np.logical_and(earth_coord_sat_id == sat_id, earth_coord_trsp_id == trsp_id)
                nb_points_trsp = np.sum(points_trsp)

                capa_ratio[points_trsp] = 1.0 / nb_points_trsp

        return earth_coord_rs * earth_coord_eff_spec * capa_ratio

    else:
        crest_capa = earth_coord_rs * earth_coord_eff_spec
        return crest_capa




        ####################################################################################################
















        #####################################################################################################
        # def normalise_user_needs(user_needs, trsp_id, sat_id):
        #    ''' this function simply normalizes a given user need vector, that would have been given in raw values
        #    (for example, a vector of datarates in MBps)
        #    '''
        #    norm_user_needs = np.zeros_like(user_needs)
        #
        #    #TODO : per transponder
        #    for j in np.unique(sat_id):
        #        for i in np.unique(trsp_id):
        #            mask_trsp = np.logical_and(trsp_id == i, sat_id == j)
        #            if np.logical_and(np.sum(mask_trsp),np.sum(user_needs[mask_trsp])) > 0:
        #                norm_user_needs[mask_trsp] = user_needs[mask_trsp] /np.sum(user_needs[mask_trsp])
        #
        #    return norm_user_needs
        #####################################################################################################
        #
        #####################################################################################################
        # def compute_capa(user_needs, eff_spec, flag_capa_calc_mode, bandwidth, trsp_id, sat_id):
        #    ''' computes capacity taking into account user needs, depending on calculation mode : '''
        #    capa = np.empty_like(user_needs)
        #
        #    for j in np.unique(sat_id):
        #        for i in np.unique(trsp_id):
        #            mask_trsp = np.logical_and(trsp_id == i, sat_id == j)
        #            if np.sum(mask_trsp) > 0:
        #                if   flag_capa_calc_mode == 'equal_no_usr_needs':
        #                    capa[mask_trsp] = eff_spec[mask_trsp] * bandwidth[mask_trsp][0]/np.size(bandwidth[mask_trsp])
        #
        #                elif flag_capa_calc_mode == 'equal_with_usr_needs':
        #                    capa[mask_trsp] = eff_spec[mask_trsp] * bandwidth[mask_trsp][0] * user_needs[mask_trsp]
        #
        #
        #    return capa
        #
        #####################################################################################################
        #
        #####################################################################################################
        # def gather_iso_frequency_transponders(central_freq, bandwidth, trsp_id):
        #
        #
        ##    list_trsp_same_color = []
        ##    mask_checked_trsps = np.empty_like(bandwidth) * 0
        #    color_nb = 1
        #    colors = np.empty_like(bandwidth) * 0
        #
        #    for i in np.arange(0,np.size(central_freq)):
        #
        #        if colors[i] == 0:
        #            curr_freq = central_freq[i]
        #            curr_bw   = bandwidth[i]
        #
        #            #find other trsps having same frequency
        #            # by "same frequency" we mean there is an overlap of freq between two transponders
        #            mask_freq_overlap = np.abs(central_freq - curr_freq) < bandwidth/2 + curr_bw/2 - 1e-8 #1e-8 is added to make sure there is no problem of overlapping borders
        ##            list_trsp_same_color.append(trsp_id[mask_freq_overlap])
        #            colors[mask_freq_overlap] = color_nb
        #            color_nb += 1
        #
        #    return colors
        #####################################################################################################

        ####################################################################################################
        # def compute_csi_intrasat(az_elev_points, trsp_id_per_point, az_elev_beam_centers, colors_per_trsp, trsp_id_per_trsp, ant_diam, freq, max_gain, flag_calc_type, theta_3dB):
        #    pass
        #    # first compute for each point all spots that will intefere significantly
        #    # at beginning : we consider all spots with same frequency are relevant
        #    # TODO : filter only spots that really have impact (to gain speed)
        #    # for determinng if spots are in same frequency : first build an array of spots in same freq
        #    for trsp in trsp_id_per_trsp:
        #        color = colors_per_trsp[trsp_id_per_trsp == trsp][0]
        #
        #        center_beams_to_consider = az_elev_beam_centers[colors_per_trsp == color]
        #
        #
        #        #compute values of sat gains for all transponder points
        #
        #        val_directivities = np.empty(np.sum(trsp_id_per_point == trsp), np.size(center_beams_to_consider)/2)
        #
        #        counter = 0
        #        for i in center_beams_to_consider:
        #            val_directivities[:,counter] = compute_sat_ant_gain(az_evel_points[trsp],ant_diam[trsp], freq[trsp], max_gain[trsp], flag_calc_type[trsp], theta_3dB[trsp])
        ##        (az_elev, ant_diam, freq, max_gain, flag_calc_type, theta_3dB):
        #
        #            counter += 1


        # then compute C/I
        # needed to prealably have recognized which directivity is the "C", and which are the interferers

####################################################################################################

####################################################################################################
# def compute_minimum_required_emitter_EIRP():
#    ''' This function computes minimum required EIRP from Emitter to achieve a given IBO
#    It then assumes maximum Satellite gain setting (i.e. min SFD) and that stations are at best possible location on coverage'''
#
#    power_at_input_section = sfd_min - ibo # TODO : look for real calculation
#
#    required_eirp = power_at_input_section - fsl_up + sat_gain_rx
#
##    nb_stations = required_eirp /
#
