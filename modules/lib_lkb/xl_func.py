# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 09:12:39 2015

*REMOVED*


MODULE
"""

from collections import OrderedDict

import numpy as np
import xlrd


# TODO : load from CSV ? (faster ?)

####################################################################################################
# def load_objects(file_name, wksheet_name):
def load_object(worksheet):
    d = OrderedDict({})
    #    #
    #    workbook = xlrd.open_workbook(file_name)
    #    worksheet = workbook.sheet_by_name(wksheet_name)
    #    #
    #
    for curr_col in range(0, worksheet.ncols):
        liste_elts = worksheet.col_values(curr_col)

        d[worksheet.cell_value(0, curr_col)] = np.array(liste_elts[1:len(liste_elts)])

    return d


####################################################################################################

####################################################################################################
def load_objects_from_xl(file_name):
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

        if wksht_name == 'SAT':
            SAT_dict = load_object(worksheet)

        if wksht_name == 'TRSP':
            TRSP_dict = load_object(worksheet)

        elif wksht_name == 'VSAT':
            VSAT_dict = load_object(worksheet)

        elif wksht_name == 'GATEWAY':
            GW_dict = load_object(worksheet)

        elif wksht_name == 'EARTH_coord_GW':
            EARTH_COORD_GW_dict = load_object(worksheet)

        elif wksht_name == 'EARTH_coord_VSAT':
            EARTH_COORD_VSAT_dict = load_object(worksheet)

        #        elif wksht_name == 'EARTH_coord_VSAT_rect':
        #            EARTH_COORD_VSAT_dict, display_dict   =   load_and_create_earth_coord_object(worksheet)

    # build display dict vsat
    display_dict_VSAT['FLAG_CONSISTENCY'] = False

    if (np.size(EARTH_COORD_VSAT_dict['LON']) > 1):
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

    # TODO : build display dict GW


    return SAT_dict, TRSP_dict, VSAT_dict, EARTH_COORD_GW_dict, GW_dict, EARTH_COORD_VSAT_dict, display_dict_VSAT


####################################################################################################



####################################################################################################
# def load_and_create_earth_coord_object(worksheet):
#    #TODO : NOT HARD CODED !!!
#    # Soon to be deprecated...
#
#    display_d={}
#    res_d = {}
#    #
##    workbook = xlrd.open_workbook(file_name)
##    worksheet = workbook.sheet_by_name(wksheet_name)
#    
#    # get values and store them in output dict (for later display)
#    for curr_row in range(1, worksheet.nrows):
#        display_d[worksheet.cell_value(curr_row,0)] = worksheet.cell_value(curr_row,1)    
#    
#    # create dictionnary
#    # TODO : check that LON, LAT, MIN, MAX and STEP are there
#    contour_zone = np.array([[display_d['LON MIN'],display_d['LAT MIN']],  \
#                             [display_d['LON MIN'],display_d['LAT MAX']],  \
#                             [display_d['LON MAX'],display_d['LAT MAX']],  \
#                             [display_d['LON MAX'],display_d['LAT MIN']] \
#                            ])
#    
#    # TODO  : save too in out dict ?
#    # TODO : do two dicts ? (might be easier for later saving)
#    display_d['xx'], display_d['yy'] = mesh_zone(contour_zone, display_d['STEP'])
#    
#    # Create dictionnary for output
#    res_d['LON'] = display_d['xx'].flatten()
#    res_d['LAT'] = display_d['yy'].flatten()
#    
#    for i in range(6,worksheet.nrows):
#        res_d[worksheet.cell_value(i,0)] = np.tile(np.array([worksheet.cell_value(i,1)]),res_d['LON'].shape)
#
#    return res_d, display_d
####################################################################################################


####################################################################################################
def dict_to_csv(my_dict, filename):
    my_items = my_dict.items()

    # open file    
    with open(filename, 'wb') as output_file:

        # first write down columns names
        my_string = str(my_items[0][0])
        for ii in range(1, len(my_items)):
            my_string = my_string + ',' + str(my_items[ii][0])
            ii += 1
        my_string = my_string + "\n"
        output_file.write(my_string)

        # then write down values names
        for i in np.arange(0, np.size(my_items[0][1])):
            my_string = str(my_items[0][1][i])
            for j in range(1, len(my_items)):
                my_string = my_string + ',' + str(my_items[j][1][i])
                j += 1
            my_string = my_string + "\n"
            output_file.write(my_string)
            i += 1

        # close file
        output_file.close()

    return output_file.closed


####################################################################################################


#####################################################################################################
# def save_to_workbook(SAT_dict, TRSP_dict, VSAT_dict, EARTH_COORD_GW_dict, GW_dict, EARTH_COORD_VSAT_dict, filename):
#    
#    workbook = xlsxwriter.Workbook(filename)
#    create_saving_worksheet(workbook, VSAT_dict, 'VSAT')
#    create_saving_worksheet(workbook, GW_dict,'GATEWAY')
#    create_saving_worksheet(workbook, SAT_dict, 'SAT')
#    create_saving_worksheet(workbook, TRSP_dict, 'TRSP')
#    create_saving_worksheet(workbook, EARTH_COORD_GW_dict, 'EARTH_coord_GW')
#    create_saving_worksheet(workbook, EARTH_COORD_VSAT_dict, 'EARTH_coord_VSAT')
#
#    workbook.close()
#####################################################################################################
#    
#    
#####################################################################################################
# def create_saving_worksheet(workbook, my_dict, wksht_name):
#
#    
#    wksht = workbook.add_worksheet(wksht_name)
#    
#    #write_keys
#    wksht.write_row(0,0,my_dict.keys())
#    # write values
#    counter = 0
#    for key in my_dict.keys():
#        wksht.write_column(1,counter,my_dict[key])
#        counter += 1
#        
#####################################################################################################    


####################################################################################################
def save_live_to_excel_file(filename, worksheet_name, perfo_dict):
    # open workbook
    # TODO : first check existence
    wb = xlwings.Book(filename)
    # open worksheet
    # TODO : first check sheet existence
    #    ws = xlwings.Sheet(worksheet_name)

    # save dict content
    fields_list = perfo_dict.keys()

    for field_item in fields_list:
        counter_col = 1
        col_list = xlwings.sheets[worksheet_name].range((1, 1), (1, 100)).value  # TODO: 100 columns limit is completely
        #  arbitrary. to replace with smthg smarter
        for col_item in col_list:
            # find column in worksheet that has same name
            if col_item == None:
                # check color format
                #                field_color, nb_format, nb_color = find_format_to_col(field_item, worksheet_name)
                #                # CALL again workbook (bug library ?!!!)
                #                #TODO : check if bug comes from library and report
                #                wb = xlwings.Workbook(filename)
                #                ws = xlwings.Sheet(worksheet_name)

                xlwings.sheets[worksheet_name].range((1, counter_col)).value = field_item
                #                xlwings.Range(ws, (1,counter_col)).color = field_color
                nb_elts = np.size(perfo_dict[field_item])
                xlwings.sheets[worksheet_name].range((2, counter_col),
                                                     (nb_elts + 1, counter_col)).value = np.atleast_2d(
                    perfo_dict[field_item]).T
                #                xlwings.Range(ws, (2,counter_col), (nb_elts+1, counter_col)).number_format = nb_format
                #                xlwings.Range(ws, (2,counter_col), (nb_elts+1, counter_col)).color = nb_color
                break  # exit for loop
            else:
                if field_item == col_item:
                    #                    field_color, nb_format, nb_color = find_format_to_col(field_item,
                    # worksheet_name)
                    #                    # CALL again workbook (bug library ?!!!)
                    #                    #TODO : check if bug comes from library and report
                    #                    wb = xlwings.Workbook(filename)
                    #                    ws = xlwings.Sheet(worksheet_name)

                    nb_elts = np.size(perfo_dict[field_item])
                    xlwings.sheets[worksheet_name].range((2, counter_col),
                                                         (nb_elts + 1, counter_col)).value = np.atleast_2d(
                        perfo_dict[field_item]).T
                    #                    xlwings.Range(ws, (2,counter_col), (nb_elts+1, counter_col)).number_format =
                    #  nb_format
                    #                    xlwings.Range(ws, (2,counter_col), (nb_elts+1, counter_col)).color = nb_color
                    break

            counter_col += 1

    wb.save()


####################################################################################################

###################################################################################################    
def find_format_to_col(field_item, tab_name):
    ''' This function applies a given format to a column for saving in excel (i.e. color of the cell, and unit)
        if the field is not found in the normal tab but in on the others, then it is a joined value and written in
        grey, using also the same format as described in the original tab
        if not found at all, then it is simply written black on white
    '''
    format_description_file = 'C:\\Users\\Damien Roques\\Desktop\\Git_test\\format.xlsx'
    tab_list = ['SAT', 'TRSP', 'VSAT', 'GATEWAY', 'EARTH_COORD_VSAT', 'EARTH_COORD_GW']

    nb_format = ''
    nb_color = None
    field_color = None

    wb1 = xlwings.Workbook(format_description_file)
    # TODO : check if sheet does exist
    ws1 = xlwings.Sheet(tab_name)

    col_list = xlwings.Range(ws1, (1, 1), (1, 100)).value  # TODO: 100 columns limit is completely arbitrary. to replace
    #  with smthg smarter
    counter = 1

    for col_item in col_list:

        #        print col_item
        if col_item == field_item:
            field_color = xlwings.Range(ws1, (1, counter)).color
            # + font color
            nb_format = xlwings.Range(ws1, (2, counter)).value
            nb_color = xlwings.Range(ws1, (2, counter)).color
            break

        counter += 1

    # TODO (?) : color joined values in grey


    return field_color, nb_format, nb_color


###################################################################################################

###################################################################################################    
def build_format_list():
    ''' This function applies a given format to a column for saving in excel (i.e. color of the cell, and unit)
        if the field is not found in the normal tab but in on the others, then it is a joined value and written in
        grey, using also the same format as described in the original tab
        if not found at all, then it is simply written black on white
    '''

    format_list = []

    format_description_file = 'C:\\Users\\Damien Roques\\Desktop\\Git_test\\format.xlsx'
    tab_list = ['SAT', 'TRSP', 'VSAT', 'GATEWAY', 'EARTH_COORD_VSAT', 'EARTH_COORD_GW']

    wb1 = xlwings.Workbook(format_description_file)

    for i in tab_list:
        ws1 = xlwings.Sheet(i)

        flag_none = False
        counter = 1
        while not (flag_none):

            value = xlwings.Range(ws1, (1, counter)).value

            if not (value == None):
                format_list.append(value)
            else:
                flag_none = True

            if counter >= 100:
                flag_none = True

            counter += 1

####################################################################################################
# def save_dict_to_structured_array(my_dict):
#    
#    
#    
#    
#    counter = 0
#    my_array =np.array([])
#    my_items = my_dict.items()
#    my_dtype = []
#    
#    for counter in range(len(my_items)):
#        
#        tpl = ((str(my_items[counter][0]),my_items[counter][1].dtype))
#        my_dtype.append(my_items[counter][1].dtype)
#
#
#    my_array = np.empty(len(my_items),dtype = my_dtype)
#
#
###        names = my_items[counter][0]
###        formats = my_items[counter][1].dtype.str
###        my_dtype = dict(names = names, formats=formats) 
###        my_col = np.array(my_items[counter][1])
###        
###        np.append(my_col, my_array)
###        
##        
##    names = my_dict.keys()
##    formats = []
##    for key in my_dict:
##        formats.append(my_dict[key].dtype.str)
###        formats.append('float64')
##
##    my_dtype = dict(names = names, formats=formats) 
###    my_array = np.array(my_dict.items(), dtype=my_dtype)    
##    my_array = np.array(np.zeros(33,40000), dtype=formats)    
###    
#    return my_array

####################################################################################################
