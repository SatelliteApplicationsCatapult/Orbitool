#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
import numpy as np
from collections import OrderedDict
import xlsxwriter


def mult2(number):
    inter = number * 2
    return inter


def load_objects_from_xl(file_name):
    """
    Loads the excel file worksheets into dictionaries

    Args:
        object: excel file names

    Returns:
        object: dictionaries
    """
    # global excel_info
    SAT_dict = {}
    TRSP_dict = {}
    VSAT_dict = {}
    EARTH_COORD_GW_dict = {}
    GW_dict = {}
    EARTH_COORD_VSAT_dict = {}
    display_dict_VSAT = {}
    # open workbook
    workbook = xlrd.open_workbook(file_name)
    # get worksheet names
    wksheets_names_list = workbook.sheet_names()

    # load objects on any wksheet
    for wksht_name in wksheets_names_list:
        worksheet = workbook.sheet_by_name(wksht_name)

        if wksht_name is 'SAT':
            SAT_dict = load_object(worksheet)

        elif wksht_name is 'TRSP':
            TRSP_dict = load_object(worksheet)

        elif wksht_name is 'VSAT':
            VSAT_dict = load_object(worksheet)

        elif wksht_name is 'GATEWAY':
            GW_dict = load_object(worksheet)

        elif wksht_name is 'EARTH_coord_GW':
            EARTH_COORD_GW_dict = load_object(worksheet)

        elif wksht_name is 'EARTH_coord_VSAT':
            EARTH_COORD_VSAT_dict = load_object(worksheet)

    # build display dict vsat
    display_dict_VSAT['FLAG_CONSISTENCY'] = False

    if np.size(EARTH_COORD_VSAT_dict['LON']) > 1:
        lon_min = np.min(EARTH_COORD_VSAT_dict['LON'])
        lon_max = np.max(EARTH_COORD_VSAT_dict['LON'])
        lat_min = np.min(EARTH_COORD_VSAT_dict['LAT'])
        lat_max = np.max(EARTH_COORD_VSAT_dict['LAT'])
        step = EARTH_COORD_VSAT_dict['LON'][1] - EARTH_COORD_VSAT_dict['LON'][
            0]  # TODO : change : not robust at all !!!

        vect_x = np.arange(lon_min, lon_max + step, step)
        vect_y = np.arange(lat_max, lat_min - step, -step)

        display_dict_VSAT['xx'], display_dict_VSAT['yy'] = np.meshgrid(vect_x, vect_y)

        if np.logical_and(np.all(np.abs(display_dict_VSAT['xx'].flatten() - EARTH_COORD_VSAT_dict['LON']) < 1e-10), \
                          np.all(np.abs(display_dict_VSAT['yy'].flatten() - EARTH_COORD_VSAT_dict['LAT']) < 1e-10)):
            display_dict_VSAT['FLAG_CONSISTENCY'] = True

    dict_to_pass = dict(SAT=SAT_dict, TRSP=TRSP_dict, VSAT=VSAT_dict, EARTH_COORD_GW=EARTH_COORD_GW_dict, GW=GW_dict,
                        EARTH_COORD_VSAT=EARTH_COORD_VSAT_dict, diplay_VSAT=display_dict_VSAT)
    return dict_to_pass


def load_object(worksheet):
    """
    Converts worksheet to dictionary
    Args:
        object: worksheet

    Returns:
        object: dictionary
    """
    d = OrderedDict()
    for curr_col in range(0, worksheet.ncols):
        liste_elts = worksheet.col_values(curr_col)

        d[worksheet.cell_value(0, curr_col)] = np.array(liste_elts[1:len(liste_elts)])

    return d


def create_saving_worksheet(filename, my_dict, wksht_name, my_dict2, wksht_name2, my_dict3, wksht_name3):
    """
    Creates an excel worksheet.
    Used in create_download() in lbController.py

    Args:
        filename:
        my_dict:
        wksht_name:

    Returns:

    """

    workbook = xlsxwriter.Workbook(filename)

    wksht = workbook.add_worksheet(wksht_name)
    # write_keys
    wksht.write_row(0, 0, my_dict.keys())
    # write values
    counter = 0
    for key in my_dict.keys():
        wksht.write_column(1, counter, my_dict[key])  # Needs to be of list format, not a single variable
        counter += 1

    wksht2 = workbook.add_worksheet(wksht_name2)
    # write_keys
    wksht2.write_row(0, 0, my_dict2.keys())
    # write values
    counter = 0
    for key in my_dict2.keys():
        wksht2.write_column(1, counter, my_dict2[key])  # Needs to be of list format, not a single variable
        counter += 1

    wksht3 = workbook.add_worksheet(wksht_name3)
    # write_keys
    wksht3.write_row(0, 0, my_dict3.keys())
    # write values
    counter = 0
    for key in my_dict3.keys():
        wksht3.write_column(1, counter, my_dict3[key])  # Needs to be of list format, not a single variable
        counter += 1
    workbook.close()
