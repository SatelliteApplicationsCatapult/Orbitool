# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 14:38:06 2015

*REMOVED*
"""


from sys import path
path.append("../modules/")
import numpy as np
from lib_lkb.utility_func import *
from lib_lkb.xl_func import *
from lib_lkb.compute_high_level_func import *


k_dB = -228.6 # Boltzmann's constant

####################################################################################################
#                                           MAIN                                                   #
####################################################################################################

#------------------------------   LOAD DATA FROM EXCEL FILE -----------------------------------------

#-------- Debug
#working_dir =   "C:\\Users\\Simon.Andersson\\PycharmProjects\\python-tools-delivery\\LKB_computation\\Examples\\TEST_constellation"

filename    =   "/home/www-data/web2py/applications/linkbudgetweb/dev/DB_Const_valide_sat_empty.xlsx"



#-------- \Debug


print('Loading input XL files...')
SAT_dict, \
TRSP_dict, \
VSAT_dict, \
EARTH_COORD_GW_dict,  \
GW_dict, \
EARTH_COORD_VSAT_dict, \
display_dict_VSAT               =   load_objects_from_xl(filename)

print('loaded !')

#---------------------------------------------------------------------------------------------------
#TODO : change definition of FWD : obliges Gateway to be emitter for example ??

#-----------------  1/ Compute SAT geometric params ------------------
#SAT_dict, nadir_ecef, pos= compute_sat_params(SAT_dict)
SAT_dict = compute_sat_params(SAT_dict)
#SAVE
print "compute_sat_params done!"


#----------------- 2/ Assign sat to each point of coverage -----------
EARTH_COORD_VSAT_dict = compute_transponder_assignment(EARTH_COORD_VSAT_dict, SAT_dict, TRSP_dict, 'FWD', 'DN')
print "compute_transponder_assignment done!"


#TODO: here needs to assign a GW to each COV point

#----------------- 3/ Compute RX/TX COV geometric params -------------------
# in that case Rx cov
EARTH_COORD_VSAT_dict = compute_coverage_points_geo_params(SAT_dict, EARTH_COORD_VSAT_dict)
print "compute_coverage_points_geo_params done!"

#----------------- 4/ Compute propag params -------------------
EARTH_COORD_VSAT_dict = compute_lkb_propag_params(EARTH_COORD_VSAT_dict, SAT_dict, TRSP_dict, VSAT_dict, 'DN', True, 'FWD')
print "compute_lkb_propag_params done!"


#----------------- 5/ Compute satellite perfos -------------------
#EARTH_COORD_VSAT_dict = compute_satellite_perfos(EARTH_COORD_VSAT_dict, TRSP_dict, 'DN')
print "compute_satellite_perfos done!"


#----------------- 6/ Compute LKB perfos -----------------------
#compute_lkb_perfos(EARTH_COORD_GW_dict,EARTH_COORD_VSAT_dict, GW_dict, VSAT_dict, 'FWD', 'disregard', 'disregard', 'disregard', 'compute', 'disregard')


print EARTH_COORD_VSAT_dict



#----------------- 7/ Export to Result file -------------------
#save_live_to_excel_file(filename, 'SAT', SAT_dict)
#save_live_to_excel_file(filename, 'EARTH_COORD_VSAT', EARTH_COORD_VSAT_dict)
#save_live_to_excel_file(filename, 'TRSP', TRSP_dict)
#save_live_to_excel_file(filename, 'GATEWAY', GW_dict)
#save_live_to_excel_file(filename, 'VSAT', VSAT_dict)
#save_live_to_excel_file(filename, 'EARTH_COORD_GW', EARTH_COORD_GW_dict)

#OLD
#save_to_workbook(SAT_dict, TRSP_dict, VSAT_dict, EARTH_COORD_GW_dict, GW_dict, EARTH_COORD_VSAT_dict, result_file)


