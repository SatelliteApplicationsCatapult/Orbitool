# -*- coding: utf-8 -*-
"""
Created on Fri Mar 06 11:52:00 2015

*REMOVED*
"""

import matplotlib.pyplot as plt

import shapefile as shp
from utility_func import *


# ------------------------------------------------------------------------------
def display_earth_ecef():
    lon = np.arange(-180.0, 180.0, 10)
    lat = np.arange(-90.0, 90.0, 10)

    (xx, yy) = np.meshgrid(lon, lat)

    xx_f = xx.flatten()
    yy_f = yy.flatten()

    vect_erf = ll_geod2ecef(np.array([xx_f, yy_f]))

    erf_x = np.reshape(vect_erf[0, :], xx.shape)
    erf_y = np.reshape(vect_erf[1, :], xx.shape)
    erf_z = np.reshape(vect_erf[2, :], xx.shape)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #    ax.plot_wireframe(vect_erf[:,0],vect_erf[:,1],vect_erf[:,2], linewidth=0.25)
    ax.plot_wireframe(erf_x, erf_y, erf_z, linewidth=0.25)
    #    ax.scatter(erf_x,erf_y,erf_z)

    return ax


# ------------------------------------------------------------------------------
#
##------------------------------------------------------------------------------    
# def display_results_on_carto(val_to_disp):
#    
#    lon = np.arange(40.0,60.0,0.5)
#    lat = np.arange(-40.0,-20.0,0.5)
#    #lon = np.arange(-180,180.0,1)
#    #lat = np.arange(-60.0,70.0,1)
#    
#    (xx,yy) = np.meshgrid(lon,lat)
#    
#    val_to_disp = np.reshape(val_to_disp, xx.shape)
#    mask = val_to_disp < 65
#    mx = np.ma.masked_array(val_to_disp, mask)
#    plt.pcolormesh(xx,yy,mx, alpha = 0.1)
##    plt.pcolor(xx,yy,val_to_disp, alpha = 0.5)
#    plt.colorbar()
##    xx_f = xx.flatten()
##    yy_f = yy.flatten()
##    res = np.array([xx_f,yy_f])
##    np.savetxt("const_lonlat.csv", res, delimiter=",")
##    np.savetxt("const_lonlat_vsat.csv", res, delimiter=",")
##    res = np.array([xx_f,yy_f]).transpose()
##------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def display_2D_world_map():
    #    filepath_data_country = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = filepath + "\data\\ne_50m_admin_0_countries\\ne_50m_admin_0_countries"
    sf = shp.Reader(filename)

    my_shapes = sf.shapes();
    poly_list = np.array([[np.nan, np.nan]])

    print('loaded')

    for i in range(0, len(my_shapes)):
        np_var = np.array(my_shapes[i].points)

        # cut polygons
        poly_ind = np.array(my_shapes[i].parts)
        np_var = np.insert(np_var, poly_ind, np.nan, axis=0)

        poly_list = np.append(poly_list, np_var, axis=0)
        #        plt.fill(np_var[:,0],np_var[:,1],'#f5f5dc', linewidth = 0.1,zorder = 0, rasterized=True)
        print (sf.record(i)[3])

    #    plt.fill(poly_list[:,0],poly_list[:,1],'#f5f5dc', linewidth = 0.1,zorder = 0, rasterized=True)

    return poly_list


# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def display_2D_sat_and_beams(az_beam_centers, elev_beam_centers, nadir_ecef, sat_pos_ecef, normal_vector, beam_radius):
    '''
    display nadir and beam centers and contours of ONE satellite
    
    '''
    # duplicate nadir as many times as number of beams (to allow for vectorized calculations)    
    nadir_ecef_disp = np.outer(nadir_ecef, np.ones(np.size(az_beam_centers)))
    pos_disp = np.outer(sat_pos_ecef, np.ones(np.size(az_beam_centers)))
    normal_vector_disp = np.outer(normal_vector, np.ones(np.size(az_beam_centers)))

    # compute ecef coord of beam centers
    points_ecef = compute_az_elev_to_ecef(np.array([az_beam_centers, elev_beam_centers]), \
                                          nadir_ecef_disp, \
                                          pos_disp, \
                                          normal_vector_disp \
                                          )

    # convert to lonlat
    beam_centers_lonlat = ecef2ll_geod(points_ecef)

    # for each beam
    beam_contour_ll = np.array([[np.nan, np.nan]]).T
    for i in np.arange(0, np.size(az_beam_centers)):
        # compute contour
        mv = compute_beam_contour(np.array([az_beam_centers, elev_beam_centers])[:, i], beam_radius[i])  # 6.7

        # convert contour in ecef and then lonlat coord
        nadir_ecef_disp = np.outer(nadir_ecef, np.ones(np.size(mv, 1)))
        pos_disp = np.outer(sat_pos_ecef, np.ones(np.size(mv, 1)))
        normal_vector_disp = np.outer(normal_vector, np.ones(np.size(mv, 1)))

        points_ecef = compute_az_elev_to_ecef(mv, \
                                              nadir_ecef_disp, \
                                              pos_disp, \
                                              normal_vector_disp \
                                              )
        mv_ll = ecef2ll_geod(points_ecef)

        # save contour with putting a "nan" between each contour
        beam_contour_ll = np.append(beam_contour_ll, np.array([[np.nan, np.nan]]).T, axis=1)
        beam_contour_ll = np.append(beam_contour_ll, mv_ll, axis=1)

    return beam_centers_lonlat, beam_contour_ll


# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def display_sat_field_of_views(nadir_ecef, sat_pos_ecef, normal_vector, sat_fov_radius, roll, pitch, yaw):
    ''' 
    display field of views of one or many satellites
    warning : sat_fov_radius is in radian already !!! (not in degrees)
    '''
    # for each beam
    sat_fov_contour_ll = np.array([[np.nan, np.nan]]).T

    nadir_ecef = np.atleast_2d(nadir_ecef)
    sat_pos_ecef = np.atleast_2d(sat_pos_ecef)
    normal_vector = np.atleast_2d(normal_vector)

    for i in np.arange(0, np.size(nadir_ecef) / 3):
        # compute contour
        mv = compute_beam_contour(np.array([0, 0]), sat_fov_radius[i])  # 6.7

        # convert contour in ecef and then lonlat coord
        nadir_ecef_disp = np.outer(nadir_ecef[:, i], np.ones(np.size(mv, 1)))
        pos_disp = np.outer(sat_pos_ecef[:, i], np.ones(np.size(mv, 1)))
        roll_disp = np.ones(np.size(mv, 1)) * roll[i]
        pitch_disp = np.ones(np.size(mv, 1)) * pitch[i]
        yaw_disp = np.ones(np.size(mv, 1)) * yaw[i]
        normal_vector_disp = np.outer(normal_vector[:, i], np.ones(np.size(mv, 1)))
        points_ecef = compute_az_elev_to_ecef(mv, \
                                              nadir_ecef_disp, \
                                              pos_disp, \
                                              normal_vector_disp, \
                                              roll=roll_disp, \
                                              pitch=pitch_disp, \
                                              yaw=yaw_disp)

        mv_ll = ecef2ll_geod(points_ecef)

        # save contour with putting a "nan" between each contour
        sat_fov_contour_ll = np.append(sat_fov_contour_ll, np.array([[np.nan, np.nan]]).T, axis=1)
        sat_fov_contour_ll = np.append(sat_fov_contour_ll, mv_ll, axis=1)

    return sat_fov_contour_ll


# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def display_sat_field_of_views_for_cesium(nadir_ecef, sat_pos_ecef, normal_vector, sat_fov_radius, roll, pitch, yaw):
    ''' 
    display field of views of one or many satellites
    warning : sat_fov_radius is in radian already !!! (not in degrees)
    '''
    # for each beam
    counter = 0

    nadir_ecef = np.atleast_2d(nadir_ecef)
    sat_pos_ecef = np.atleast_2d(sat_pos_ecef)
    normal_vector = np.atleast_2d(normal_vector)

    for i in np.arange(0, np.size(nadir_ecef) / 3):
        # compute contour
        mv = compute_beam_contour(sat_fov_radius[i])  # 6.7

        # convert contour in ecef and then lonlat coord
        nadir_ecef_disp = np.outer(nadir_ecef[:, i], np.ones(np.size(mv, 1)))
        pos_disp = np.outer(sat_pos_ecef[:, i], np.ones(np.size(mv, 1)))
        roll_disp = np.ones(np.size(mv, 1)) * roll[i]
        pitch_disp = np.ones(np.size(mv, 1)) * pitch[i]
        yaw_disp = np.ones(np.size(mv, 1)) * yaw[i]
        normal_vector_disp = np.outer(normal_vector[:, i], np.ones(np.size(mv, 1)))
        points_ecef = compute_az_elev_to_ecef(mv, \
                                              nadir_ecef_disp, \
                                              pos_disp, \
                                              normal_vector_disp, \
                                              roll=roll_disp, \
                                              pitch=pitch_disp, \
                                              yaw=yaw_disp)

        mv_ll = ecef2ll_geod(points_ecef)
        # TODO : ADD XYZ

        # save contour
        if counter == 0:
            sat_fov_contour_ll = mv_ll
        else:
            sat_fov_contour_ll = np.vstack((sat_fov_contour_ll, mv_ll))

        counter += 1

    return sat_fov_contour_ll


# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
def display_2D_sat_and_beams_for_cesium(SAT_ID, sat_ids, sat_pl_ids, nadir_ecef, sat_pos_ecef, normal_vector, roll, pitch, yaw, \
                                        trsp_pl_ids, trsp_rot_x, trsp_rot_y, trsp_rot_z, trsp_beams_radius):
    '''
    display nadir and beam centers and contours of ONE satellite

    CAREFUL : SAT_ID is a string !!! Only works for integer sat IDs though

    '''
    # first convert to string if not already done the various IDs
    if not (sat_ids.dtype.char == 'S'):
        sat_ids = sat_ids.astype('int').astype('string')

    if not (type(SAT_ID) == np.ndarray):
        SAT_ID = str(int(SAT_ID))
    else:
        if not (SAT_ID.dtype.char == 'S'):
            SAT_ID = SAT_ID.astype('int').astype('string')

    # find right satellite and right parameters of the SAT_dict to use
    index_satellite = np.flatnonzero(sat_ids == SAT_ID)
    # if no satellite found break
    if np.size(index_satellite) == 0:
        print('NO SAT FOUND')
        return np.array([]), np.array([])

    # TODO : check if the following is necessary (what happens if the user only inputs data for ONE sat)
    nadir_ecef = nadir_ecef[:, index_satellite]
    sat_pos_ecef = sat_pos_ecef[:, index_satellite]
    normal_vector = normal_vector[:, index_satellite]

    # extract from TRSP_dict the parameters corresponding to this transponder
    payload_id_of_sat = sat_pl_ids[index_satellite]
    roll = roll[index_satellite]
    pitch = pitch[index_satellite]
    yaw = yaw[index_satellite]
    beam_radius = trsp_beams_radius[trsp_pl_ids == payload_id_of_sat]
    rot_x = trsp_rot_x[trsp_pl_ids == payload_id_of_sat]
    rot_y = trsp_rot_y[trsp_pl_ids == payload_id_of_sat]
    rot_z = trsp_rot_z[trsp_pl_ids == payload_id_of_sat]

    # for each beam
    counter = 0
    beam_contour_ll = np.array([[np.nan, np.nan]]).T
    for i in np.arange(0, np.size(rot_x)):
        # compute contour
        mv = compute_beam_contour(np.array(beam_radius[i]))  # 6.7

        # convert contour in ecef and then lonlat coord
        nadir_ecef_disp = np.outer(nadir_ecef, np.ones(np.size(mv, 1)))
        pos_disp = np.outer(sat_pos_ecef, np.ones(np.size(mv, 1)))
        normal_vector_disp = np.outer(normal_vector, np.ones(np.size(mv, 1)))

        points_ecef = compute_az_elev_to_ecef(mv, \
                                              nadir_ecef_disp, \
                                              pos_disp, \
                                              normal_vector_disp, \
                                              roll, \
                                              pitch, \
                                              yaw, \
                                              rot_x[i], \
                                              rot_y[i], \
                                              rot_z[i])

        mv_ll = ecef2ll_geod(points_ecef)

        # save contour
        if counter == 0:
            beam_contour_ll = mv_ll
        else:
            beam_contour_ll = np.vstack((beam_contour_ll, mv_ll))

        counter += 1
        #        #save contour with putting a "nan" between each contour
        #        beam_contour_ll = np.append(beam_contour_ll, np.array([[np.nan,np.nan]]).T, axis=1)
        #        beam_contour_ll = np.append(beam_contour_ll, mv_ll, axis=1)

    return beam_contour_ll

# ------------------------------------------------------------------------------
