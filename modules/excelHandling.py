#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
import numpy as np
from collections import OrderedDict

def mult2(number):
    inter = number * 2
    return inter

def load_objects_from_xl(file_name):

    """
    Loads the excel file worksheets into dictionaries

    Returns:
        object:
    """
    SAT_dict={}
    TRSP_dict={}
    VSAT_dict={}
    EARTH_COORD_GW_dict={}
    GW_dict={}
    EARTH_COORD_VSAT_dict = {}
    display_dict_VSAT = {}
    # open workbook
    workbook = xlrd.open_workbook(file_name)
    # get worksheet names
    wksheets_names_list = workbook.sheet_names()

    # load objects on any wksheet
    for wksht_name in wksheets_names_list:
        worksheet = workbook.sheet_by_name(wksht_name)

        if wksht_name    ==   'SAT':
            SAT_dict                              =   load_object(worksheet)

        if wksht_name    ==   'TRSP':
            TRSP_dict                              =   load_object(worksheet)

        elif wksht_name  ==   'VSAT':
            VSAT_dict                             =   load_object(worksheet)

        elif wksht_name ==   'GATEWAY':
            GW_dict                               =   load_object(worksheet)

        elif wksht_name ==   'EARTH_coord_GW':
            EARTH_COORD_GW_dict                   =   load_object(worksheet)

        elif wksht_name ==   'EARTH_coord_VSAT':
            EARTH_COORD_VSAT_dict                 =   load_object(worksheet)

#        elif wksht_name == 'EARTH_coord_VSAT_rect':
#            EARTH_COORD_VSAT_dict, display_dict   =   load_and_create_earth_coord_object(worksheet)

    # build display dict vsat
    display_dict_VSAT['FLAG_CONSISTENCY'] = False

    if (np.size(EARTH_COORD_VSAT_dict['LON']) > 1):
        lon_min = np.min(EARTH_COORD_VSAT_dict['LON'])
        lon_max = np.max(EARTH_COORD_VSAT_dict['LON'])
        lat_min = np.min(EARTH_COORD_VSAT_dict['LAT'])
        lat_max = np.max(EARTH_COORD_VSAT_dict['LAT'])
        step = EARTH_COORD_VSAT_dict['LON'][1] - EARTH_COORD_VSAT_dict['LON'][0] #TODO : change : not robust at all !!!

        vect_x = np.arange(lon_min, lon_max+step, step)
        vect_y = np.arange(lat_max, lat_min-step, -step)

        display_dict_VSAT['xx'], display_dict_VSAT['yy'] = np.meshgrid(vect_x, vect_y)



        if np.logical_and(np.all(np.abs(display_dict_VSAT['xx'].flatten() - EARTH_COORD_VSAT_dict['LON'])<1e-10), \
                          np.all(np.abs(display_dict_VSAT['yy'].flatten() - EARTH_COORD_VSAT_dict['LAT'])<1e-10)):

            display_dict_VSAT['FLAG_CONSISTENCY'] = True


    # TODO : build display dict GW


    return SAT_dict, TRSP_dict, VSAT_dict, EARTH_COORD_GW_dict,  GW_dict, EARTH_COORD_VSAT_dict, display_dict_VSAT


def load_object(worksheet):
    """

    workbook = xlrd.open_workbook(file_name)
    worksheet = workbook.sheet_by_name(wksheet_name)

    Returns:
        object:
    """
    d=OrderedDict({})
    for curr_col in range(0, worksheet.ncols):
        liste_elts = worksheet.col_values(curr_col)

        d[worksheet.cell_value(0,curr_col)] = np.array(liste_elts[1:len(liste_elts)])

    return d

def compute_sat_params(SAT_dict, flag_intermediate_params=False):
    '''
    This function computes main satellite characteristics, needed for other
    calculation :
    - nadir in ECEF coordinates
    - satellite position in ECEF coordinates

    It's from Damien code

    Returns:
        object:
    '''

    nadir                    =   np.array([SAT_dict['NADIR_LON'],SAT_dict['NADIR_LAT']])


    nadir_ecef               =   ll_geod2ecef(nadir) # switch to ecef set of coordinates
    SAT_dict['NADIR_X_ECEF'] =   nadir_ecef[0]   
    SAT_dict['NADIR_Y_ECEF'] =   nadir_ecef[1]   
    SAT_dict['NADIR_Z_ECEF'] =   nadir_ecef[2]   


    pos                      =   compute_sat_position(nadir_ecef, SAT_dict['DISTANCE'])
    SAT_dict['SAT_POS_X_ECEF']   =   pos[0]
    SAT_dict['SAT_POS_Y_ECEF']   =   pos[1]
    SAT_dict['SAT_POS_Z_ECEF']   =   pos[2]


    normal_vector              =   compute_normal_vector(SAT_dict['INCLINATION_ANGLE']*np.pi/180, nadir_ecef, SAT_dict['FLAG_ASC_DESC'])
    SAT_dict['NORMAL_VECT_X']   =   normal_vector[0]
    SAT_dict['NORMAL_VECT_Y']   =   normal_vector[1]
    SAT_dict['NORMAL_VECT_Z']   =   normal_vector[2]



    if flag_intermediate_params:
        return SAT_dict, nadir_ecef, pos, normal_vector
    else:
        return SAT_dict

def create_saving_worksheet(filename, my_dict, wksht_name):
    import xlsxwriter

    workbook = xlsxwriter.Workbook(filename)
    wksht = workbook.add_worksheet(wksht_name)

    #write_keys
    wksht.write_row(0,0,my_dict.keys())
    # write values
    counter = 0
    for key in my_dict.keys():
        wksht.write_column(1,counter,my_dict[key]) #Needs to be of list format, not a single variable
        counter += 1
    workbook.close()
