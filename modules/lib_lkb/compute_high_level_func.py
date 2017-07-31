# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 18:00:23 2015

***REMOVED***
"""
import logging
logger = logging.getLogger("web2py.app.myweb2pyapplication")
logger.setLevel(logging.DEBUG)

from sys import path

path.append("../../")
import numpy as np
from lib_lkb.utility_func import *
from lib_lkb.xl_func import *
from lib_lkb.geometric_func import *
import platform
if platform.system() == 'Windows':
    _lib = p.windll.LoadLibrary(pathtopropa)
elif platform.system() == 'Linux':
    _lib = p.cdll.LoadLibrary(pathtopropa)
from lib_lkb.propa_func import *
############################################################################################################################
def compute_sat_params(SAT_dict, flag_intermediate_params=False):
    ''' This function computes main satellite characteristics, needed for other
    calculation :
    - nadir in ECEF coordinates
    - satellite position in ECEF coordinates
    '''

    nadir = np.array([SAT_dict['NADIR_LON'], SAT_dict['NADIR_LAT']])

    nadir_ecef = ll_geod2ecef(nadir)  # switch to ecef set of coordinates
    SAT_dict['NADIR_X_ECEF'] = nadir_ecef[0]
    SAT_dict['NADIR_Y_ECEF'] = nadir_ecef[1]
    SAT_dict['NADIR_Z_ECEF'] = nadir_ecef[2]

    pos = compute_sat_position(nadir_ecef, SAT_dict['DISTANCE'])
    SAT_dict['SAT_POS_X_ECEF'] = pos[0]
    SAT_dict['SAT_POS_Y_ECEF'] = pos[1]
    SAT_dict['SAT_POS_Z_ECEF'] = pos[2]

    normal_vector = compute_normal_vector(SAT_dict['INCLINATION_ANGLE'] * np.pi / 180, nadir_ecef,
                                          SAT_dict['FLAG_ASC_DESC'])
    SAT_dict['NORMAL_VECT_X'] = normal_vector[0]
    SAT_dict['NORMAL_VECT_Y'] = normal_vector[1]
    SAT_dict['NORMAL_VECT_Z'] = normal_vector[2]

    if flag_intermediate_params:
        return SAT_dict, nadir_ecef, pos, normal_vector
    else:
        return SAT_dict


############################################################################################################################

############################################################################################################################
def compute_transponder_assignment(EARTH_COORD_dict, SAT_dict, TRSP_dict, flag_fwd_return, flag_uplink_downlink):
    ''' This function wraps the function allowing to assign a transponder to each point on Earth
    '''

    # first select the right transponders depending on FWD_RTN
    if (flag_fwd_return == 'FWD'):

        mask_trsp_to_use = (TRSP_dict['FWD_RTN_FLAG'] == 'FWD')

    else:

        mask_trsp_to_use = (TRSP_dict['FWD_RTN_FLAG'] == 'RTN')

    if (flag_uplink_downlink == 'UP'):
        az_beam_ctrs = TRSP_dict['BEAM_RX_CENTER_Y_ANT'][mask_trsp_to_use] * -1 * np.pi / 180
        elev_beam_ctrs = TRSP_dict['BEAM_RX_CENTER_X_ANT'][mask_trsp_to_use] * np.pi / 180

    else:
        az_beam_ctrs = TRSP_dict['BEAM_TX_CENTER_Y_ANT'][mask_trsp_to_use] * -1 * np.pi / 180
        elev_beam_ctrs = TRSP_dict['BEAM_TX_CENTER_X_ANT'][mask_trsp_to_use] * np.pi / 180

    # we only select here the satellites that are not considered as interferers
    mask_no_interf = (SAT_dict['INTERF_FLAG'] == 'NO')

    nadir_ecef = np.array([SAT_dict['NADIR_X_ECEF'][mask_no_interf], \
                           SAT_dict['NADIR_Y_ECEF'][mask_no_interf], \
                           SAT_dict['NADIR_Z_ECEF'][mask_no_interf]])

    pos = np.array([SAT_dict['SAT_POS_X_ECEF'][mask_no_interf], \
                    SAT_dict['SAT_POS_Y_ECEF'][mask_no_interf], \
                    SAT_dict['SAT_POS_Z_ECEF'][mask_no_interf]])

    normal_vector = np.array([SAT_dict['NORMAL_VECT_X'][mask_no_interf], \
                              SAT_dict['NORMAL_VECT_Y'][mask_no_interf], \
                              SAT_dict['NORMAL_VECT_Z'][mask_no_interf]])

    # TODO : take into account FWD RETURN FLAG !! (?)
    # TODO : refine code below more properly
    # (lon, lat) 2  ECEF
    vect_ecef = ll_geod2ecef(np.array([EARTH_COORD_dict['LON'], EARTH_COORD_dict['LAT']]))
    #    EARTH_COORD_dict['POS_X_ECEF'] = vect_ecef[0]
    #    EARTH_COORD_dict['POS_Y_ECEF'] = vect_ecef[1]
    #    EARTH_COORD_dict['POS_Z_ECEF'] = vect_ecef[2]

    EARTH_COORD_dict['SAT_ID'], \
    EARTH_COORD_dict['TRSP_ID'] = assign_transponder3(vect_ecef, \
                                                      pos, \
                                                      nadir_ecef, \
                                                      normal_vector, \
                                                      SAT_dict['SAT_ID'][mask_no_interf], \
                                                      sat_pl_id=SAT_dict['PAYLOAD_ID'][mask_no_interf], \
                                                      trsp_az_ant=az_beam_ctrs, \
                                                      trsp_el_ant=elev_beam_ctrs, \
                                                      trsp_id=TRSP_dict['TRSP_ID'], \
                                                      trsp_pl_id=TRSP_dict['PAYLOAD_ID'])

    #    assign_transponder_test(vect_ecef, \
    #                            pos, \
    #                            nadir_ecef, \
    #                            normal_vector, \
    #                            SAT_dict['SAT_ID'][mask_no_interf], \
    #                            sat_pl_id = SAT_dict['PAYLOAD_ID'][mask_no_interf], \
    #                            trsp_x_angle = TRSP_dict['PAYLOAD_ID'], \
    #                            trsp_y_angle = np.array([0.0]), \
    #                            trsp_z_angle = np.array([0.0]), \
    #                            trsp_id = TRSP_dict['TRSP_ID'], \
    #                            trsp_pl_id = TRSP_dict['PAYLOAD_ID'])
    #    EARTH_COORD_dict['SAT_ID'], EARTH_COORD_dict['TRSP_ID'], el    =   assign_transponder2(vect_ecef, \
    #                                                                                      pos, \
    #                                                                                      SAT_dict['SAT_ID'], \
    #                                                                                      trsp_az_ant = az_beam_ctrs, \
    #                                                                                      trsp_el_ant = elev_beam_ctrs, \
    #                                                                                      trsp_id = TRSP_dict['TRSP_ID'])
    #    EARTH_COORD_dict['SAT_ID'], EARTH_COORD_dict['TRSP_ID']    =   assign_transponder(EARTH_COORD_dict['LON'], EARTH_COORD_dict['LAT'], \
    #                                                                                      pos, \
    #                                                                                      nadir_ecef, normal_vector, SAT_dict['SAT_ID'], \
    #                                                                                      az_beam_ctrs, elev_beam_ctrs, TRSP_dict['TRSP_ID'])

    # add payload id
    EARTH_COORD_dict['PAYLOAD_ID'] = db_join(EARTH_COORD_dict, SAT_dict, 'PAYLOAD_ID', 'SAT_ID')

    return EARTH_COORD_dict


############################################################################################################################



############################################################################################################################
def compute_coverage_points_geo_params(SAT_dict, EARTH_COORD_dict, TRSP_dict, flag_uplink_downlink):
    ''' This function computes geometric parameters of coverage points,
    that are needed for most calculations :
    - coord
    - dist
    - elevation
    -
    '''

    #    # first select the right transponders depending on FWD_RTN
    #    if (flag_fwd_return == 'FWD'):
    #
    #        mask_trsp_to_use = (TRSP_dict['FWD_RTN_FLAG'] == 'FWD')
    #
    #    else:
    #
    #        mask_trsp_to_use = (TRSP_dict['FWD_RTN_FLAG'] == 'RTN')
    #


    vect_ecef = ll_geod2ecef(np.array([EARTH_COORD_dict['LON'], EARTH_COORD_dict['LAT']]))

    EARTH_COORD_dict['POS_X_ECEF'] = vect_ecef[0]
    EARTH_COORD_dict['POS_Y_ECEF'] = vect_ecef[1]
    EARTH_COORD_dict['POS_Z_ECEF'] = vect_ecef[2]

    EARTH_COORD_dict['SAT_POS_X_ECEF'] = db_join(EARTH_COORD_dict, SAT_dict, 'SAT_POS_X_ECEF', 'SAT_ID')
    EARTH_COORD_dict['SAT_POS_Y_ECEF'] = db_join(EARTH_COORD_dict, SAT_dict, 'SAT_POS_Y_ECEF', 'SAT_ID')
    EARTH_COORD_dict['SAT_POS_Z_ECEF'] = db_join(EARTH_COORD_dict, SAT_dict, 'SAT_POS_Z_ECEF', 'SAT_ID')

    # TODO : change of function to put with Link perfos ?
    EARTH_COORD_dict['DIST'] = compute_distance_to_sat(EARTH_COORD_dict['POS_X_ECEF'], \
                                                       EARTH_COORD_dict['POS_Y_ECEF'], \
                                                       EARTH_COORD_dict['POS_Z_ECEF'], \
                                                       EARTH_COORD_dict['SAT_POS_X_ECEF'], \
                                                       EARTH_COORD_dict['SAT_POS_Y_ECEF'], \
                                                       EARTH_COORD_dict['SAT_POS_Z_ECEF'])

    EARTH_COORD_dict['ELEVATION'] = compute_elev_grd_wrap(EARTH_COORD_dict['LON'], \
                                                          EARTH_COORD_dict['LAT'], \
                                                          EARTH_COORD_dict['SAT_POS_X_ECEF'], \
                                                          EARTH_COORD_dict['SAT_POS_Y_ECEF'], \
                                                          EARTH_COORD_dict['SAT_POS_Z_ECEF'])
    # TODO : remove function compute_elev_grd_wrap to simplify code

    # compute points of coverage in antenna coordinate system, in az/elev ******************************************************
    EARTH_COORD_dict['NADIR_X_ECEF'] = db_join(EARTH_COORD_dict, SAT_dict, 'NADIR_X_ECEF', 'SAT_ID')
    EARTH_COORD_dict['NADIR_Y_ECEF'] = db_join(EARTH_COORD_dict, SAT_dict, 'NADIR_Y_ECEF', 'SAT_ID')
    EARTH_COORD_dict['NADIR_Z_ECEF'] = db_join(EARTH_COORD_dict, SAT_dict, 'NADIR_Z_ECEF', 'SAT_ID')

    EARTH_COORD_dict['NORMAL_VECT_X'] = db_join(EARTH_COORD_dict, SAT_dict, 'NORMAL_VECT_X', 'SAT_ID')
    EARTH_COORD_dict['NORMAL_VECT_Y'] = db_join(EARTH_COORD_dict, SAT_dict, 'NORMAL_VECT_Y', 'SAT_ID')
    EARTH_COORD_dict['NORMAL_VECT_Z'] = db_join(EARTH_COORD_dict, SAT_dict, 'NORMAL_VECT_Z', 'SAT_ID')

    EARTH_COORD_dict['ROLL'] = db_join(EARTH_COORD_dict, SAT_dict, 'ROLL', 'SAT_ID')
    EARTH_COORD_dict['PITCH'] = db_join(EARTH_COORD_dict, SAT_dict, 'PITCH', 'SAT_ID')
    EARTH_COORD_dict['YAW'] = db_join(EARTH_COORD_dict, SAT_dict, 'YAW', 'SAT_ID')

    nadir_ecef_per_cov_point = np.array(
        [EARTH_COORD_dict['NADIR_X_ECEF'], EARTH_COORD_dict['NADIR_Y_ECEF'], EARTH_COORD_dict['NADIR_Z_ECEF']])

    sat_pos_ecef_per_cov_point = np.array(
        [EARTH_COORD_dict['SAT_POS_X_ECEF'], EARTH_COORD_dict['SAT_POS_Y_ECEF'], EARTH_COORD_dict['SAT_POS_Z_ECEF']])

    normal_vect_ecef_per_cov_point = np.array(
        [EARTH_COORD_dict['NORMAL_VECT_X'], EARTH_COORD_dict['NORMAL_VECT_Y'], EARTH_COORD_dict['NORMAL_VECT_Z']])

    if (flag_uplink_downlink == 'DN'):

        ROT_X_ANT = db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_TX_CENTER_X_ANT', ['PAYLOAD_ID', 'TRSP_ID'])
        ROT_Y_ANT = db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_TX_CENTER_Y_ANT', ['PAYLOAD_ID', 'TRSP_ID'])
        ROT_Z_ANT = db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_TX_CENTER_Z_ANT', ['PAYLOAD_ID', 'TRSP_ID'])

    else:

        ROT_X_ANT = db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_RX_CENTER_X_ANT', ['PAYLOAD_ID', 'TRSP_ID'])
        ROT_Y_ANT = db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_RX_CENTER_Y_ANT', ['PAYLOAD_ID', 'TRSP_ID'])
        ROT_Z_ANT = db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_RX_CENTER_Z_ANT', ['PAYLOAD_ID', 'TRSP_ID'])




        # TODO :  more efficient to do it by satellite ?

    ecef_points = ll_geod2ecef(np.array([EARTH_COORD_dict['LON'], EARTH_COORD_dict['LAT']]))

    az_elev_points = compute_ecef_to_az_elev(ecef_points, \
                                             nadir_ecef_per_cov_point, \
                                             sat_pos_ecef_per_cov_point, \
                                             normal_vect_ecef_per_cov_point, \
                                             roll=EARTH_COORD_dict['ROLL'] * np.pi / 180, \
                                             pitch=EARTH_COORD_dict['PITCH'] * np.pi / 180, \
                                             yaw=EARTH_COORD_dict['YAW'] * np.pi / 180, \
                                             Rx=ROT_X_ANT * np.pi / 180, \
                                             Ry=ROT_Y_ANT * np.pi / 180, \
                                             Rz=ROT_Z_ANT * np.pi / 180)  # TODO : add Rx, Ry, Rz

    #                                                roll = EARTH_COORD_dict['ROLL'], \
    #                                                pitch = EARTH_COORD_dict['PITCH'], \
    #                                                yaw = EARTH_COORD_dict['YAW'])

    #    az_elev_points    = compute_ecef_to_az_elev(EARTH_COORD_dict['LON'], \
    #                                                    EARTH_COORD_dict['LAT'], \
    #                                                    nadir_ecef_per_cov_point, \
    #                                                    sat_pos_ecef_per_cov_point, \
    #                                                    normal_vect_ecef_per_cov_point)
    #

    if (flag_uplink_downlink == 'DN'):
        EARTH_COORD_dict['AZ_ANT_DN'] = az_elev_points[0]
        EARTH_COORD_dict['ELEV_ANT_DN'] = az_elev_points[1]
    else:
        EARTH_COORD_dict['AZ_ANT_UP'] = az_elev_points[0]
        EARTH_COORD_dict['ELEV_ANT_UP'] = az_elev_points[1]

    return EARTH_COORD_dict


############################################################################################################################

############################################################################################################################
def compute_lkb_propag_params(EARTH_COORD_dict, SAT_dict, TRSP_dict, TERMINAL_dict, flag_uplink_downlink, flag_propag,
                              flag_fwd_rtn):
    '''
    This function computes all the necessary parameters for assessing the performances of the downlink :
    - Free Space Loss
    - Propag (based on CNES dll)
    - Satellite Gain
    - + (TODO) G/T // EIRP ???

    '''

    # ------------------------------   CALCULATIONS OF PROPAG + FSL PARAMS -----------------------------------------


    if (flag_uplink_downlink == 'DN'):
        EARTH_COORD_dict['CENTRAL_FQ_DN'] = db_join(EARTH_COORD_dict, TRSP_dict, 'CENTRAL_FQ_DN',
                                                    ['PAYLOAD_ID', 'TRSP_ID'])
        EARTH_COORD_dict['FSL_DN'] = compute_fsl(EARTH_COORD_dict['DIST'], EARTH_COORD_dict['CENTRAL_FQ_DN'])



    else:
        EARTH_COORD_dict['CENTRAL_FQ_UP'] = db_join(EARTH_COORD_dict, TRSP_dict, 'CENTRAL_FQ_UP',
                                                    ['PAYLOAD_ID', 'TRSP_ID'])
        EARTH_COORD_dict['FSL_UP'] = compute_fsl(EARTH_COORD_dict['DIST'], EARTH_COORD_dict['CENTRAL_FQ_UP'])

    if (flag_propag == True):
        if ((flag_fwd_rtn == 'FWD' and flag_uplink_downlink == 'DN') or (
                flag_fwd_rtn == 'RTN' and flag_uplink_downlink == 'UP')):  # this implies that VSAT is always Rx for RTN...
            EARTH_COORD_dict['POLAR'] = db_join(EARTH_COORD_dict, TERMINAL_dict, 'POLAR', 'VSAT_ID')  # @!!! BUG
            EARTH_COORD_dict['DIAMETER'] = db_join(EARTH_COORD_dict, TERMINAL_dict, 'DIAMETER', 'VSAT_ID')  # @!!! BUG
            EARTH_COORD_dict['EFFICIENCY'] = db_join(EARTH_COORD_dict, TERMINAL_dict, 'EFFICIENCY',
                                                     'VSAT_ID')  # @!!! BUG
            EARTH_COORD_dict['POLAR_TILT_ANGLE'] = compute_polar_tilt_angle(EARTH_COORD_dict['POLAR'])

        else:  # this implies that GW is always Tx for RTN // Rx for FWD...
            EARTH_COORD_dict['POLAR'] = db_join(EARTH_COORD_dict, TERMINAL_dict, 'POLAR', 'GW_ID')  # @!!! BUG
            EARTH_COORD_dict['DIAMETER'] = db_join(EARTH_COORD_dict, TERMINAL_dict, 'DIAMETER', 'GW_ID')  # @!!! BUG
            EARTH_COORD_dict['EFFICIENCY'] = db_join(EARTH_COORD_dict, TERMINAL_dict, 'EFFICIENCY', 'GW_ID')  # @!!! BUG
            EARTH_COORD_dict['POLAR_TILT_ANGLE'] = compute_polar_tilt_angle(EARTH_COORD_dict['POLAR'])

        if (flag_uplink_downlink == 'UP'):
            EARTH_COORD_dict['PROPAG_UP'] = compute_propag(EARTH_COORD_dict['LON'], \
                                                           EARTH_COORD_dict['LAT'], \
                                                           EARTH_COORD_dict['ALT'], \
                                                           EARTH_COORD_dict['ELEVATION'], \
                                                           EARTH_COORD_dict['CENTRAL_FQ_UP'], \
                                                           EARTH_COORD_dict['POLAR_TILT_ANGLE'], \
                                                           EARTH_COORD_dict['DIAMETER'], \
                                                           EARTH_COORD_dict['EFFICIENCY'], \
                                                           EARTH_COORD_dict['AVAILABILITY_UP'], \
                                                           )
        else:
            EARTH_COORD_dict['PROPAG_DN'] = compute_propag(EARTH_COORD_dict['LON'], \
                                                           EARTH_COORD_dict['LAT'], \
                                                           EARTH_COORD_dict['ALT'], \
                                                           EARTH_COORD_dict['ELEVATION'], \
                                                           EARTH_COORD_dict['CENTRAL_FQ_DN'], \
                                                           EARTH_COORD_dict['POLAR_TILT_ANGLE'], \
                                                           EARTH_COORD_dict['DIAMETER'], \
                                                           EARTH_COORD_dict['EFFICIENCY'], \
                                                           EARTH_COORD_dict['AVAILABILITY_DN'], \
                                                           )
        return EARTH_COORD_dict
        ############################################################################################################################


############################################################################################################################
def compute_satellite_perfos(EARTH_COORD_dict, TRSP_dict, flag_uplink_downlink):
    ''' This function computes the satellite performances on either uplink or downlink (need to be called twice if both link need to be computed)
    It will compute and output the satellite EIRP / or G/T on every point on Earth defined by the EARTH_COORD_dict
    '''

    # ------------------------------   CALCULATION ON SAT GAIN Rx or Tx, and then EIRP or G/T  -----------------------------------------

    if flag_uplink_downlink == 'UP':
        az_elev_points = np.array([EARTH_COORD_dict['AZ_ANT_UP'], EARTH_COORD_dict['ELEV_ANT_UP']])
    else:
        az_elev_points = np.array([EARTH_COORD_dict['AZ_ANT_DN'], EARTH_COORD_dict['ELEV_ANT_DN']])

    if (flag_uplink_downlink == 'DN'):

        #        # Join centers of beams in (az,elev)
        #        EARTH_COORD_dict['BEAM_TX_CENTER_AZ_ANT']    =   db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_TX_CENTER_AZ_ANT', ['PAYLOAD_ID', 'TRSP_ID'])
        #        EARTH_COORD_dict['BEAM_TX_CENTER_EL_ANT']    =   db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_TX_CENTER_EL_ANT', ['PAYLOAD_ID', 'TRSP_ID'])
        #    #TODO : option LONLAT
        #    #EARTH_COORD_dict = db_join(EARTH_COORD_dict, SAT_dict, 'BEAM_RX_CENTER_LON', 'TRSP_ID')
        #    #EARTH_COORD_dict = db_join(EARTH_COORD_dict, SAT_dict, 'BEAM_RX_CENTER_LAT', 'TRSP_ID')
        #
        #        az_elev_beam_centers_tx                      =   np.array([EARTH_COORD_dict['BEAM_TX_CENTER_AZ_ANT']*np.pi/180,EARTH_COORD_dict['BEAM_TX_CENTER_EL_ANT']*np.pi/180])
        #

        # compute points coord in antenna coordinates
        points_ant_coord_tx = az_elev_points  # translate_az_elev_sc_to_az_elev_ant(az_elev_beam_centers_tx, az_elev_points)
        # compute maximum gain
        TRSP_dict['MAX_GAIN_TX'] = compute_max_gain(TRSP_dict['BEAM_TX_EFF'], TRSP_dict['BEAM_TX_ANT_DIAM'],
                                                    TRSP_dict['CENTRAL_FQ_DN'], TRSP_dict['BEAM_TX_TYPE'])

        # join params to compute radiation pattern
        EARTH_COORD_dict['BEAM_TX_ANT_DIAM'] = db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_TX_ANT_DIAM',
                                                       ['PAYLOAD_ID', 'TRSP_ID'])
        EARTH_COORD_dict['BEAM_TX_TYPE'] = db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_TX_TYPE',
                                                   ['PAYLOAD_ID', 'TRSP_ID'])
        EARTH_COORD_dict['MAX_GAIN_TX'] = db_join(EARTH_COORD_dict, TRSP_dict, 'MAX_GAIN_TX', ['PAYLOAD_ID', 'TRSP_ID'])
        EARTH_COORD_dict['BEAM_TX_THETA_3DB'] = db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_TX_THETA_3DB',
                                                        ['PAYLOAD_ID', 'TRSP_ID'])

        # compute radiation pattern and gain on every point of the coverage
        EARTH_COORD_dict['SAT_GAIN_TX'] = compute_sat_ant_gain(points_ant_coord_tx,
                                                               EARTH_COORD_dict['BEAM_TX_ANT_DIAM'], \
                                                               EARTH_COORD_dict['CENTRAL_FQ_DN'], \
                                                               EARTH_COORD_dict['MAX_GAIN_TX'], \
                                                               EARTH_COORD_dict['BEAM_TX_TYPE'], \
                                                               EARTH_COORD_dict['BEAM_TX_THETA_3DB'])

        # Compute EIRP of satellite
        EARTH_COORD_dict['IBO'] = db_join(EARTH_COORD_dict, TRSP_dict, 'IBO', ['PAYLOAD_ID', 'TRSP_ID'])
        EARTH_COORD_dict['AMP_SAT'] = db_join(EARTH_COORD_dict, TRSP_dict, 'AMP_SAT', ['PAYLOAD_ID', 'TRSP_ID'])
        EARTH_COORD_dict['OBO'] = compute_OBO(
            EARTH_COORD_dict['IBO'])  # TODO :this function is only a stub at the moment
        EARTH_COORD_dict['SAT_EIRP'] = compute_EIRP(EARTH_COORD_dict['AMP_SAT'], EARTH_COORD_dict['OBO'],
                                                    EARTH_COORD_dict['SAT_GAIN_TX'])



    else:

        #        EARTH_COORD_dict['BEAM_RX_CENTER_AZ_ANT']     =   db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_RX_CENTER_AZ_ANT', ['PAYLOAD_ID', 'TRSP_ID'])
        #        EARTH_COORD_dict['BEAM_RX_CENTER_EL_ANT']     =   db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_RX_CENTER_EL_ANT', ['PAYLOAD_ID', 'TRSP_ID'])
        #
        #
        #        az_elev_beam_centers_rx                       =   np.array([EARTH_COORD_dict['BEAM_RX_CENTER_AZ_ANT']*np.pi/180,EARTH_COORD_dict['BEAM_RX_CENTER_EL_ANT']*np.pi/180])



        points_ant_coord_rx = az_elev_points  # translate_az_elev_sc_to_az_elev_ant(az_elev_beam_centers_rx, az_elev_points)

        TRSP_dict['MAX_GAIN_RX'] = compute_max_gain(TRSP_dict['BEAM_RX_EFF'], TRSP_dict['BEAM_RX_ANT_DIAM'],
                                                    TRSP_dict['CENTRAL_FQ_UP'], TRSP_dict['BEAM_RX_TYPE'])

        EARTH_COORD_dict['BEAM_RX_ANT_DIAM'] = db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_RX_ANT_DIAM',
                                                       ['PAYLOAD_ID', 'TRSP_ID'])
        EARTH_COORD_dict['BEAM_RX_TYPE'] = db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_RX_TYPE',
                                                   ['PAYLOAD_ID', 'TRSP_ID'])
        EARTH_COORD_dict['MAX_GAIN_RX'] = db_join(EARTH_COORD_dict, TRSP_dict, 'MAX_GAIN_RX', ['PAYLOAD_ID', 'TRSP_ID'])
        EARTH_COORD_dict['BEAM_RX_THETA_3DB'] = db_join(EARTH_COORD_dict, TRSP_dict, 'BEAM_RX_THETA_3DB',
                                                        ['PAYLOAD_ID', 'TRSP_ID'])

        EARTH_COORD_dict['SAT_GAIN_RX'] = compute_sat_ant_gain(points_ant_coord_rx,
                                                               EARTH_COORD_dict['BEAM_RX_ANT_DIAM'], \
                                                               EARTH_COORD_dict['CENTRAL_FQ_UP'], \
                                                               EARTH_COORD_dict['MAX_GAIN_RX'], \
                                                               EARTH_COORD_dict['BEAM_RX_TYPE'], \
                                                               EARTH_COORD_dict['BEAM_RX_THETA_3DB'])

        # compute satellite G/T
        EARTH_COORD_dict['SYS_TEMP'] = db_join(EARTH_COORD_dict, TRSP_dict, 'SYS_TEMP', ['PAYLOAD_ID', 'TRSP_ID'])
        EARTH_COORD_dict['SAT_GPT'] = EARTH_COORD_dict['SAT_GAIN_RX'] - 10 * np.log10(EARTH_COORD_dict['SYS_TEMP'])

    return EARTH_COORD_dict


############################################################################################################################


############################################################################################################################
def compute_lkb_CsN0_perfos(EARTH_COORD_TX_dict, EARTH_COORD_RX_dict, TX_TERMINAL_dict, RX_terminal_dict, fwd_rtn_flag,
                            csn0_up_flag, \
                            csi0_up_flag, \
                            csim0_flag, \
                            csn0_dn_flag, \
                            csi0_dn_flag):
    ############## INSTANTIATE AND COMPUTE ALL THE LKB PARAMETERS
    if (csn0_up_flag != 'from_file'):
        EARTH_COORD_TX_dict['CSN0_UP'] = np.ones_like(EARTH_COORD_TX_dict['LON']) * 999
    if (csi0_up_flag != 'from_file'):
        EARTH_COORD_TX_dict['CSI0_UP'] = np.ones_like(EARTH_COORD_TX_dict['LON']) * 999
    if (csim0_flag != 'from_file'):
        EARTH_COORD_RX_dict['CSIM0'] = np.ones_like(EARTH_COORD_RX_dict['LON']) * 999
    if (csn0_dn_flag != 'from_file'):
        EARTH_COORD_RX_dict['CSN0_DN'] = np.ones_like(EARTH_COORD_RX_dict['LON']) * 999
    if (csi0_dn_flag != 'from_file'):
        EARTH_COORD_RX_dict['CSI0_DN'] = np.ones_like(EARTH_COORD_RX_dict['LON']) * 999

    # compute C/N0up
    if csn0_up_flag == 'compute':
        # compute C/N0 uplink
        # Hypothesis: EIRP MAX !!!
        if fwd_rtn_flag == 'FWD':  # !!! This line implies that GW is necessarily Tx in FWD // VSAT is necessarily Tx in RTN
            EARTH_COORD_TX_dict['EIRP'] = db_join(EARTH_COORD_TX_dict, TX_TERMINAL_dict, 'EIRP', 'GW_ID')
        else:
            EARTH_COORD_TX_dict['EIRP'] = db_join(EARTH_COORD_TX_dict, TX_TERMINAL_dict, 'EIRP', 'VSAT_ID')

        EARTH_COORD_TX_dict['CSN0_UP'] = compute_CSN0_UP(EARTH_COORD_TX_dict['EIRP'], EARTH_COORD_TX_dict['FSL_UP'],
                                                         EARTH_COORD_TX_dict['PROPAG_UP'],
                                                         EARTH_COORD_TX_dict['SAT_GPT'])
        # join C/N0 uplink to RESULT dict

    # compute C/N0dn
    if csn0_dn_flag == 'compute':
        # compute C/N0 downlink
        if fwd_rtn_flag == 'FWD':  # !!! This line implies that GW is necessarily Rx in RTN // VSAT is necessarily Rx in FWD
            EARTH_COORD_RX_dict['GPT'] = db_join(EARTH_COORD_RX_dict, RX_terminal_dict, 'GPT', 'VSAT_ID')
        else:
            EARTH_COORD_RX_dict['GPT'] = db_join(EARTH_COORD_RX_dict, RX_terminal_dict, 'GPT', 'GW_ID')

        EARTH_COORD_RX_dict['CSN0_DN'] = compute_CSN0_DN(EARTH_COORD_RX_dict['SAT_EIRP'], EARTH_COORD_RX_dict['FSL_DN'],
                                                         EARTH_COORD_RX_dict['PROPAG_DN'], EARTH_COORD_RX_dict['GPT'])

    # TODO : compute C/I0up, C/I0dn, C/Im(0)


    # compute C/Ntotal
    if fwd_rtn_flag == 'FWD':

        EARTH_COORD_RX_dict['CSN0_UP'] = db_join(EARTH_COORD_RX_dict, EARTH_COORD_TX_dict, 'CSN0_UP',
                                                 ['SAT_ID', 'PAYLOAD_ID', 'TRSP_ID'], default_value=999)
        EARTH_COORD_RX_dict['CSI0_UP'] = db_join(EARTH_COORD_RX_dict, EARTH_COORD_TX_dict, 'CSI0_UP',
                                                 ['SAT_ID', 'PAYLOAD_ID', 'TRSP_ID'], default_value=999)
        EARTH_COORD_RX_dict['CSN0_TOT'] = compute_csn0_total(EARTH_COORD_RX_dict['CSN0_UP'], \
                                                             EARTH_COORD_RX_dict['CSI0_UP'], \
                                                             EARTH_COORD_RX_dict['CSIM0'], \
                                                             EARTH_COORD_RX_dict['CSI0_DN'], \
                                                             EARTH_COORD_RX_dict['CSN0_DN'])

    else:
        EARTH_COORD_TX_dict['CSN0_DN'] = db_join(EARTH_COORD_TX_dict, EARTH_COORD_RX_dict, 'CSN0_DN',
                                                 ['SAT_ID', 'PAYLOAD_ID', 'TRSP_ID'], default_value=999)
        EARTH_COORD_TX_dict['CSI0_DN'] = db_join(EARTH_COORD_TX_dict, EARTH_COORD_RX_dict, 'CSI0_DN',
                                                 ['SAT_ID', 'PAYLOAD_ID', 'TRSP_ID'], default_value=999)
        EARTH_COORD_TX_dict['CSIM0'] = db_join(EARTH_COORD_TX_dict, EARTH_COORD_RX_dict, 'CSIM0',
                                               ['SAT_ID', 'PAYLOAD_ID', 'TRSP_ID'], default_value=999)
        EARTH_COORD_TX_dict['CSN0_TOT'] = compute_csn0_total(EARTH_COORD_TX_dict['CSN0_UP'], \
                                                             EARTH_COORD_TX_dict['CSI0_UP'], \
                                                             EARTH_COORD_TX_dict['CSIM0'], \
                                                             EARTH_COORD_TX_dict['CSI0_DN'], \
                                                             EARTH_COORD_TX_dict['CSN0_DN'])


############################################################################################################################


############################################################################################################################
def compute_lkb_CsN_perfos(EARTH_COORD_TX_dict, EARTH_COORD_RX_dict, TRSP_dict, TX_terminal_dict, fwd_rtn_flag):
    # TODO : RTN
    # TODO : think of the best way to keep calculations when GW params are not defined



    # Take into account roll-of factor from waveform
    if fwd_rtn_flag == 'FWD':
        # apply strategy for using power and frequency band
        # on FWD link : assumption is to use all available power from GW, and band from TRSP
        # There is NO modelling of (min, max) SFD in this simplified model
        EARTH_COORD_TX_dict['ROLL_OFF'] = db_join(EARTH_COORD_TX_dict, TX_terminal_dict, 'ROLL_OFF', 'GW_ID')
        EARTH_COORD_TX_dict['BANDWIDTH'] = db_join(EARTH_COORD_TX_dict, TRSP_dict, 'BANDWIDTH',
                                                   ['PAYLOAD_ID', 'TRSP_ID'])
        EARTH_COORD_TX_dict['RS'] = EARTH_COORD_TX_dict['BANDWIDTH'] * (1 - EARTH_COORD_TX_dict['ROLL_OFF'])
        # Append bandwidth
        EARTH_COORD_RX_dict['RS'] = db_join(EARTH_COORD_RX_dict, EARTH_COORD_TX_dict, 'RS', ['PAYLOAD_ID', 'TRSP_ID'],
                                            default_value=0)

    else:  # RTN case
        # Here : take into account Rs from terminal, and use all available power\
        EARTH_COORD_TX_dict['RS'] = db_join(EARTH_COORD_TX_dict, TX_terminal_dict, 'RS', 'VSAT_ID')

    # convert C/N0up to C/Nup
    if fwd_rtn_flag == 'FWD':
        if not (np.all(EARTH_COORD_RX_dict['CSN0_UP'] == 999 * np.ones_like(EARTH_COORD_RX_dict['CSN0_UP']))):
            EARTH_COORD_RX_dict['CSN_UP'] = EARTH_COORD_RX_dict['CSN0_UP'] - 10 * np.log10(
                EARTH_COORD_RX_dict['RS']) - 60
    else:
        if not (np.all(EARTH_COORD_TX_dict['CSN0_UP'] == 999 * np.ones_like(EARTH_COORD_TX_dict['CSN0_UP']))):
            EARTH_COORD_TX_dict['CSN_UP'] = EARTH_COORD_TX_dict['CSN0_UP'] - 10 * np.log10(
                EARTH_COORD_TX_dict['RS']) - 60

    # convert C/N0dn to C/N0dn
    if fwd_rtn_flag == 'FWD':
        if not (np.all(EARTH_COORD_RX_dict['CSN0_DN'] == np.ones_like(EARTH_COORD_RX_dict['CSN0_DN']))):
            EARTH_COORD_RX_dict['CSN_DN'] = EARTH_COORD_RX_dict['CSN0_DN'] - 10 * np.log10(
                EARTH_COORD_RX_dict['RS']) - 60
    else:
        if not (np.all(EARTH_COORD_TX_dict['CSN0_DN'] == np.ones_like(EARTH_COORD_TX_dict['CSN0_DN']))):
            EARTH_COORD_TX_dict['CSN_DN'] = EARTH_COORD_TX_dict['CSN0_DN'] - 10 * np.log10(
                EARTH_COORD_TX_dict['RS']) - 60

    # TODO : same for C/I(up,dn) and C/Im

    # convert C/N0total to C/N0total
    if fwd_rtn_flag == 'FWD':
        if not (np.all(EARTH_COORD_RX_dict['CSN0_TOT'] == np.ones_like(EARTH_COORD_RX_dict['CSN0_TOT']))):
            EARTH_COORD_RX_dict['CSN_TOT'] = EARTH_COORD_RX_dict['CSN0_TOT'] - 10 * np.log10(
                EARTH_COORD_RX_dict['RS']) - 60
    else:
        if not (np.all(EARTH_COORD_TX_dict['CSN0_TOT'] == np.ones_like(EARTH_COORD_TX_dict['CSN0_TOT']))):
            EARTH_COORD_TX_dict['CSN_TOT'] = EARTH_COORD_TX_dict['CSN0_TOT'] - 10 * np.log10(
                EARTH_COORD_TX_dict['RS']) - 60


############################################################################################################################


############################################################################################################################
def compute_spectral_efficiency_and_capacity(EARTH_COORD_RX_dict, flag_waveform, flag_fwd_rtn):
    EARTH_COORD_RX_dict['SPEC_EFF'] = compute_eff_spec(EARTH_COORD_RX_dict['CSN_TOT'], flag_waveform)

    # TODO : compute for each sat,payload, trsp, how many users are in the beam
    #    EARTH_COORD_RX_dict['TOTAL_MAX_CAPA']    =   EARTH_COORD_RX_dict['RS'] * EARTH_COORD_RX_dict['SPEC_EFF']


    EARTH_COORD_RX_dict['USR_CAPA'] = compute_capacity(EARTH_COORD_RX_dict['TRSP_ID'], EARTH_COORD_RX_dict['SAT_ID'],
                                                       EARTH_COORD_RX_dict['RS'], EARTH_COORD_RX_dict['SPEC_EFF'],
                                                       flag_fwd_rtn)
############################################################################################################################
















# TODO : compute C/I // C/Im parameters

############# compute C/N0 total
# TODO
#    if fwd_rtn_flag == 'FWD':
#        EARTH_COORD_RX_dict                          =   db_join(EARTH_COORD_RX_dict, EARTH_COORD_TX_dict, 'CSN0_UP', 'GW_ID')
#        EARTH_COORD_RX_dict                          =   db_join(EARTH_COORD_RX_dict, EARTH_COORD_TX_dict, 'CSI0_UP', 'GW_ID')
#
#        EARTH_COORD_RX_dict['CSN0_TOTAL']            =   compute_csn0_total(EARTH_COORD_RX_dict['CSN0_UP'], \
#                                                                    EARTH_COORD_RX_dict['CSI0_UP'], \
#                                                                    EARTH_COORD_RX_dict['CSIM0'], \
#                                                                    EARTH_COORD_RX_dict['CSN0_DN'], \
#                                                                    EARTH_COORD_RX_dict['CSI0_DN'])
#
#    else:
#        EARTH_COORD_TX_dict                          =   db_join(EARTH_COORD_TX_dict, EARTH_COORD_RX_dict, 'CSN0_DN', 'GW_ID')
#        EARTH_COORD_TX_dict                          =   db_join(EARTH_COORD_TX_dict, EARTH_COORD_RX_dict, 'CSI0_DN', 'GW_ID')
#        EARTH_COORD_TX_dict                          =   db_join(EARTH_COORD_TX_dict, EARTH_COORD_RX_dict, 'CSIM0', 'GW_ID')
#
#        EARTH_COORD_TX_dict['CSN0_TOTAL']            =   compute_csn0_total(EARTH_COORD_TX_dict['CSN0_UP'], \
#                                                                    EARTH_COORD_TX_dict['CSI0_UP'], \
#                                                                    EARTH_COORD_TX_dict['CSIM0'], \
#                                                                    EARTH_COORD_TX_dict['CSN0_DN'], \
#                                                                    EARTH_COORD_TX_dict['CSI0_DN'])
#############################################################################################################################




