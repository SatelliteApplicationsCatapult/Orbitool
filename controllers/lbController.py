# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is the Link Budget Controller
# -------------------------------------------------------------------------
from excelHandling import *
import numpy as np
from gluon import *
import os
from lib_lkb.propa_func import *
from lib_lkb.functions_to_use import *
from lib_lkb.xl_func import *
from lib_lkb.compute_high_level_func import *
from lib_lkb.display_func import *
import subprocess
from collections import OrderedDict


import logging
logger = logging.getLogger("web2py.app.linkbudgetweb")
logger.setLevel(logging.DEBUG)


response.title = 'Link Budget Calculator'


def index():
    """ Home Page """
    return dict(message=T('Multi-Mission Satellite Link Budget Analysis Framework'))


def about():
    """ About page """
    return dict(message=T('About'))

def input():
    """ Input form """ #TODO: Think about adding drag and drop plugin
    session.job = ""
    record = dbLinkBudget.Job(request.args(0))

    dbLinkBudget.Job.Date.readable = False


    dbLinkBudget.Job.simulator_mode.readable = False
    dbLinkBudget.Job.simulator_mode.writable = False
    dbLinkBudget.Job.sat_geo_params.readable = False
    dbLinkBudget.Job.sat_geo_params.writable = False
    dbLinkBudget.Job.points2trsp.readable = False
    dbLinkBudget.Job.points2trsp.writable = False
    dbLinkBudget.Job.sat_fov.writable = False
    dbLinkBudget.Job.sat_fov.readable = False
    dbLinkBudget.Job.trsp_fov.writable = False
    dbLinkBudget.Job.trsp_fov.readable = False
    dbLinkBudget.Job.points2trsp.readable = False
    dbLinkBudget.Job.points2trsp.writable = False
    dbLinkBudget.Job.gw2trsp.readable = False
    dbLinkBudget.Job.gw2trsp.writable = False
    dbLinkBudget.Job.comp_point_cover.readable = False
    dbLinkBudget.Job.comp_point_cover.writable = False
    dbLinkBudget.Job.comp_gw_cover.readable = False
    dbLinkBudget.Job.comp_gw_cover.writable = False
    dbLinkBudget.Job.propa_feeder_link.readable = False
    dbLinkBudget.Job.propa_feeder_link.writable = False
    dbLinkBudget.Job.propa_user_link.readable = False
    dbLinkBudget.Job.propa_user_link.writable = False
    dbLinkBudget.Job.sat_up_perf.readable = False
    dbLinkBudget.Job.sat_up_perf.writable = False
    dbLinkBudget.Job.sat_dwn_perf.readable = False
    dbLinkBudget.Job.sat_dwn_perf.writable = False
    dbLinkBudget.Job.comp_link_budget.readable = False
    dbLinkBudget.Job.comp_link_budget.writable = False
    dbLinkBudget.Job.processed.readable = False
    dbLinkBudget.Job.processed.writable = False
    dbLinkBudget.Job.csn0_up_flag.readable = False
    dbLinkBudget.Job.csn0_up_flag.writable = False
    dbLinkBudget.Job.csim0_flag.readable = False
    dbLinkBudget.Job.csim0_flag.writable = False
    dbLinkBudget.Job.csn0_dn_flag.readable = False
    dbLinkBudget.Job.csn0_dn_flag.writable = False
    dbLinkBudget.Job.csi0_dn_flag.readable = False
    dbLinkBudget.Job.csi0_dn_flag.writable = False
    dbLinkBudget.Job.csi0_dn_flag.readable = False
    dbLinkBudget.Job.csi0_dn_flag.writable = False
    dbLinkBudget.Job.csi0_up_flag.readable = False
    dbLinkBudget.Job.csi0_up_flag.writable = False
    dbLinkBudget.Job.csn0_dn_flag.readable = False
    dbLinkBudget.Job.csn0_dn_flag.writable = False

    form = SQLFORM(dbLinkBudget.Job, record, deletable=True,
                    upload=URL('download'), formstyle='table3cols')
    if form.process().accepted:
        session.flash = "%s - %s has been accepted" % (form.vars.id, form.vars.job_name)
        session.job = form.vars.job_name
        add_excel_2_db()
    else:
        session.flash = "%s - %s has FAILED" % (form.vars.id, form.vars.job_name)
    return dict(form=form)


def test_crud():
    """ Test Function used to test code before major use """
    return dict(a=0)


def select():
    """  Page which renders a JQuery Datatable to let you select entries  """
    import json
    job = json.dumps(dbLinkBudget(dbLinkBudget.Job).select().as_list(),
                     default=json_serial)  # Formatting need to interface with JQuery Datatables
    return dict(job=XML(job))

def update():
    """
    Update form
    This function creates the update form and
    creates dictionaries to be viewed on the right hand side of the page.
    Returns:
        JSON formatted stream

    """
    import json
    job = json.dumps(dbLinkBudget(dbLinkBudget.Job).select().as_list(),
                     default=json_serial)  # default json.dumps specificed
    gw = []
    vsat = []
    sat = []
    trsp = []
    for row in dbLinkBudget(dbLinkBudget.Earth_coord_GW.Job_ID == request.args(0)).iterselect(groupby='GW_ID'): #this looks for the different types of gateway referred to in gw Earth_coord
        gw.extend(dbLinkBudget(dbLinkBudget.Gateway.GW_ID == row['GW_ID']).select().as_list())

    for row in dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.Job_ID == request.args(0)).iterselect(groupby='VSAT_ID'):  #this looks for the different types of vsat referred to in vsat Earth_coord
        vsat.extend(dbLinkBudget(dbLinkBudget.VSAT.VSAT_ID == row['VSAT_ID']).select().as_list())

    for row in dbLinkBudget(dbLinkBudget.Earth_coord_GW.Job_ID == request.args(0)).iterselect(groupby='SAT_ID'): #this looks for the different types of Satellite referred to in gateway Earth_coord
        sat.extend(dbLinkBudget(dbLinkBudget.SAT.SAT_ID == row['SAT_ID']).select().as_list())

    for row in dbLinkBudget(dbLinkBudget.Earth_coord_GW.Job_ID == request.args(0)).iterselect(groupby='PAYLOAD_ID'): #this looks for the different types of payload referred to in gateway Earth_coord and outputs transponder information
        trsp.extend(dbLinkBudget(dbLinkBudget.TRSP.PAYLOAD_ID == row['PAYLOAD_ID']).select().as_list())

    record = dbLinkBudget.Job(request.args(0))
    dbLinkBudget.Job.Date.readable = False

    dbLinkBudget.Job.file_up.writable = False
    dbLinkBudget.Job.file_up.readable = False

    dbLinkBudget.Job.simulator_mode.readable = False
    dbLinkBudget.Job.simulator_mode.writable = False
    dbLinkBudget.Job.sat_geo_params.readable = False
    dbLinkBudget.Job.sat_geo_params.writable = False
    dbLinkBudget.Job.points2trsp.readable = False
    dbLinkBudget.Job.points2trsp.writable = False
    dbLinkBudget.Job.gw2trsp.readable = False
    dbLinkBudget.Job.gw2trsp.writable = False
    dbLinkBudget.Job.comp_point_cover.readable = False
    dbLinkBudget.Job.comp_point_cover.writable = False
    dbLinkBudget.Job.comp_gw_cover.readable = False
    dbLinkBudget.Job.comp_gw_cover.writable = False
    dbLinkBudget.Job.propa_feeder_link.readable = False
    dbLinkBudget.Job.propa_feeder_link.writable = False
    dbLinkBudget.Job.propa_user_link.readable = False
    dbLinkBudget.Job.propa_user_link.writable = False
    dbLinkBudget.Job.sat_up_perf.readable = False
    dbLinkBudget.Job.sat_up_perf.writable = False
    dbLinkBudget.Job.sat_dwn_perf.readable = False
    dbLinkBudget.Job.sat_dwn_perf.writable = False
    dbLinkBudget.Job.comp_link_budget.readable = False
    dbLinkBudget.Job.comp_link_budget.writable = False
    dbLinkBudget.Job.processed.readable = False
    dbLinkBudget.Job.processed.writable = False

    dbLinkBudget.Job.csn0_up_flag.readable = False
    dbLinkBudget.Job.csn0_up_flag.writable = False
    dbLinkBudget.Job.csim0_flag.readable = False
    dbLinkBudget.Job.csim0_flag.writable = False
    dbLinkBudget.Job.csn0_dn_flag.readable = False
    dbLinkBudget.Job.csn0_dn_flag.writable = False
    dbLinkBudget.Job.csi0_dn_flag.readable = False
    dbLinkBudget.Job.csi0_dn_flag.writable = False
    dbLinkBudget.Job.csi0_dn_flag.readable = False
    dbLinkBudget.Job.csi0_dn_flag.writable = False
    dbLinkBudget.Job.csi0_up_flag.readable = False
    dbLinkBudget.Job.csi0_up_flag.writable = False
    dbLinkBudget.Job.csn0_dn_flag.readable = False
    dbLinkBudget.Job.csn0_dn_flag.writable = False

#    dbLinkBudget.Job.processed.readable = False # enable these when in use. Having it off is good for debugging
#    dbLinkBudget.Job.processed.writable = False
    form = SQLFORM(dbLinkBudget.Job, record, deletable=True, formstyle='table3cols', submit_button='Update')
    form.add_button('Next', URL('launch', args=request.args(0)))
    if form.process().accepted:
        session.flash = "%s - %s has been updated" % (form.vars.id, form.vars.job_name)
        if form.deleted:
            session.flash = "%s) %s has been deleted" % (form.vars.id, form.vars.job_name)
            redirect(URL('select'))
        else:
            session.job = form.vars.job_name
    return dict(job=XML(job), vsat=XML(json.dumps(vsat)), gw=XML(json.dumps(gw)), sat=XML(json.dumps(sat)), trsp=XML(json.dumps(trsp)), form=form)

def launch():
    """
    Run page


    """
    record = dbLinkBudget.Job(request.args(0))
    dbLinkBudget.Job.Date.readable = False

    dbLinkBudget.Job.file_up.writable = False
    dbLinkBudget.Job.file_up.readable = False
    dbLinkBudget.Job.job_name.writable = False
    dbLinkBudget.Job.description.writable = False
    dbLinkBudget.Job.sat_fov.show_if = (dbLinkBudget.Job.sat_geo_params==True)
    dbLinkBudget.Job.trsp_fov.show_if = (dbLinkBudget.Job.sat_geo_params==True)
    dbLinkBudget.Job.propa_feeder_link.show_if = (dbLinkBudget.Job.comp_gw_cover==True)
    dbLinkBudget.Job.propa_user_link.show_if = (dbLinkBudget.Job.comp_point_cover==True)
    dbLinkBudget.Job.sat_up_perf.show_if = (dbLinkBudget.Job.sat_geo_params==True)
    dbLinkBudget.Job.sat_dwn_perf.show_if = (dbLinkBudget.Job.sat_geo_params==True)
    #dbLinkBudget.Job.comp_link_budget.show_if = (dbLinkBudget.Job.propa_feeder_link==True)

    dbLinkBudget.Job.csn0_up_flag.show_if = (dbLinkBudget.Job.comp_link_budget==True)
    dbLinkBudget.Job.csi0_up_flag.show_if = (dbLinkBudget.Job.comp_link_budget==True)
    dbLinkBudget.Job.csim0_flag.show_if = (dbLinkBudget.Job.comp_link_budget==True)
    dbLinkBudget.Job.csn0_dn_flag.show_if = (dbLinkBudget.Job.comp_link_budget==True)
    dbLinkBudget.Job.csi0_dn_flag.show_if = (dbLinkBudget.Job.comp_link_budget==True)
    #    dbLinkBudget.Job.processed.readable = False # enable these when in use. Having it off is good for debugging
#    dbLinkBudget.Job.processed.writable = False
    form = SQLFORM(dbLinkBudget.Job, record, deletable=True, formstyle='table3cols', submit_button='Save')
    form.add_button('Select Page', URL('select'))
    if form.process().accepted:
        session.flash = "%s - %s has been updated" % (form.vars.id, form.vars.job_name)
        if form.deleted:
            session.flash = "%s) %s has been deleted" % (form.vars.id, form.vars.job_name)
            redirect(URL('select'))
        else:
            session.job = form.vars.job_name
    return dict(form=form)

def add_excel_2_db():
    """
    Function used to insert excel dictionary into database

    """
    file = dbLinkBudget.Job(dbLinkBudget.Job.job_name == session.job).file_up  # Find uploaded file
    job_id = dbLinkBudget.Job(dbLinkBudget.Job.job_name == session.job).id
    [SAT_dict, TRSP_dict, VSAT_dict, EARTH_COORD_GW_dict, GW_dict, EARTH_COORD_VSAT_dict,
     display_dict_VSAT] = load_objects_from_xl(os.path.join(request.folder, 'uploads', file))
    #----save csv test
    #import time
    #timestr = time.strftime("%Y%m%d-%H%M%S")
    #filename = 'applications/linkbudgetweb/arrays/propa_input_array-'+timestr+'.txt'
    #np.savetxt(filename, np.column_stack((EARTH_COORD_VSAT_dict['LON'], \
    #                                                                      EARTH_COORD_VSAT_dict['LAT'],\
    #                                                                      )))
    ##-----------------  1/ Compute SAT geometric params ------------------
    #SAT_dict = compute_sat_params(SAT_dict)
    ##----------------- 2/ Assign sat to each point of coverage -----------
    #dbLinkBudget.Job.simulator_mode == 'FWD'
    #EARTH_COORD_VSAT_dict = compute_transponder_assignment(EARTH_COORD_VSAT_dict, SAT_dict, TRSP_dict, 'FWD', 'DN')
    ##----------------- 3/ Compute RX/TX COV geometric params -------------------
    #EARTH_COORD_VSAT_dict = compute_coverage_points_geo_params(SAT_dict, EARTH_COORD_VSAT_dict)
    ##----------------- 4/ Compute propag params -------------------
    #EARTH_COORD_VSAT_dict = compute_lkb_propag_params(EARTH_COORD_VSAT_dict, SAT_dict, TRSP_dict, VSAT_dict, 'DN', True, 'FWD')
    ##----------------- 5/ Compute satellite perfos -------------------
    #EARTH_COORD_VSAT_dict = compute_satellite_perfos(EARTH_COORD_VSAT_dict, TRSP_dict, 'DN')
    #read_array_to_db(dbLinkBudget.VSAT, VSAT_dict)
    read_array_to_db(dbLinkBudget.Gateway, GW_dict)
    read_array_to_db(dbLinkBudget.TRSP, TRSP_dict)
    read_array_to_db(dbLinkBudget.SAT, SAT_dict)
    read_array_to_db(dbLinkBudget.Earth_coord_GW, EARTH_COORD_GW_dict, job_id)
    read_array_to_db(dbLinkBudget.EARTH_coord_VSAT, EARTH_COORD_VSAT_dict, job_id)
    #TODO: could add a table for display_dict_VSAT
    #EXTRACT THE DICTS TO HAVE A LOOK AT THEM
#    np.save('/tmp/picklefile',EARTH_COORD_VSAT_dict.keys())
#    import pickle
#    with open('/tmp/picklefile1', 'wb') as handle:
#      pickle.dump(EARTH_COORD_VSAT_dict.keys(), handle)
    redirect(URL('update', args=job_id))


def read_array_to_db(db, ordDict, job_id=0):
    """
    Used to read in dictionaries which contain
    np arrays created when reading excel file

    Args:
        db: database
        ordDict: OrderedDict
        job_id:

    """
    temp = ordDict.fromkeys(ordDict, 0)
    if job_id:  # Check for tables which require records to be assigned with job_id number
        temp['Job_ID'] = job_id
    for i in range(ordDict.values()[0].size):
        for j in range(len(ordDict.keys())):
            temp[ordDict.keys()[j]] = ordDict.values()[j][i]
        db.update_or_insert(**temp)  # Update/Insert state used to create new database records. Checks if all the fields are filled in + updates, else inserts. Might just change this to update

def read_db_to_array(db, job_id=0):
    """
    Used to read from the db and output
    dictionaries which contain
    np arrays, same as inputted from the excel file

    Args:
        db: database
        job_id:

    """
    SAT_dict=OrderedDict({})
    TRSP_dict=OrderedDict({})
    VSAT_dict=OrderedDict({})
    EARTH_COORD_GW_dict=OrderedDict({})
    GW_dict=OrderedDict({})
    EARTH_COORD_VSAT_dict=OrderedDict({})
    display_dict_VSAT==OrderedDict({})

    gw=[]
    for field in dbLinkBudget.Gateway:
        for row in dbLinkBudget(dbLinkBudget.Earth_coord_GW.Job_ID == request.args(0)).iterselect(groupby='GW_ID'): #this looks for the different types of gateway referred to in gw Earth_coord
            gw.extend(dbLinkBudget(dbLinkBudget.Gateway.GW_ID == row['GW_ID']).select(field).as_list())

    #d=OrderedDict({})
    for curr_col in range(0, worksheet.ncols):
        liste_elts = worksheet.col_values(curr_col)

        d[worksheet.cell_value(0,curr_col)] = np.array(liste_elts[1:len(liste_elts)])

    return d

def json_serial(obj):
    """
    Function needed to serialise the date field for json output

    Args:
        obj:


    """
    from datetime import datetime
    if isinstance(obj, datetime):
        serial = obj.strftime("%d-%m-%Y  %H:%M")
        return serial
    raise TypeError("Type not serializable")


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]

    Returns:
        object:
    """
    return response.download(request, dbLinkBudget)


def create_download():
    """
    Creates downloadable file.
    This is called in update.html under options

    TODO: consider using lists instead of dicionaries so that the download excel is ordered.
    TODO: at RX fields
    """
    #VSAT
    rowt = dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.Job_ID == request.args(0)).iterselect("LON",
"LAT",
"COUNTRY",
"SEA_LAND",
"VSAT_ID",
"ALT",
"AVAILABILITY_UP",
"AVAILABILITY_DN",
"USER_NEED",
"SAT_ID",
"TRSP_ID",
"PAYLOAD_ID",
"POS_X_ECEF",
"POS_Y_ECEF",
"POS_Z_ECEF",
"SAT_POS_X_ECEF",
"SAT_POS_Y_ECEF",
"SAT_POS_Z_ECEF",
"DIST",
"ELEVATION",
"NADIR_X_ECEF",
"NADIR_Y_ECEF",
"NADIR_Z_ECEF",
"NORMAL_VECT_X",
"NORMAL_VECT_Y",
"NORMAL_VECT_Z",
"ROLL",
"PITCH",
"YAW",
"AZ_SC",
"ELEV_SC",
"CENTRAL_FQ_DN",
"FSL_DN",
"POLAR",
"DIAMETER",
"EFFICIENCY",
"POLAR_TILT_ANGLE",
"PROPAG_DN",
"BEAM_TX_CENTER_AZ_ANT",
"BEAM_TX_CENTER_EL_ANT",
"BEAM_TX_ANT_DIAM",
"BEAM_TX_TYPE",
"MAX_GAIN_TX",
"BEAM_TX_THETA_3DB",
"SAT_GAIN_TX",
"IBO",
"AMP_SAT",
"OBO",
"SAT_EIRP","CSIM0","CSN0_DN","CSI0_DN","GPT").first().as_dict()

    vsat = OrderedDict.fromkeys(rowt["_extra"])
    for key in vsat.keys():
        vsat[key] = []
    for row in dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.Job_ID == request.args(0)).iterselect("LON",
"LAT",
"COUNTRY",
"SEA_LAND",
"VSAT_ID",
"ALT",
"AVAILABILITY_UP",
"AVAILABILITY_DN",
"USER_NEED",
"SAT_ID",
"TRSP_ID",
"PAYLOAD_ID",
"POS_X_ECEF",
"POS_Y_ECEF",
"POS_Z_ECEF",
"SAT_POS_X_ECEF",
"SAT_POS_Y_ECEF",
"SAT_POS_Z_ECEF",
"DIST",
"ELEVATION",
"NADIR_X_ECEF",
"NADIR_Y_ECEF",
"NADIR_Z_ECEF",
"NORMAL_VECT_X",
"NORMAL_VECT_Y",
"NORMAL_VECT_Z",
"ROLL",
"PITCH",
"YAW",
"AZ_SC",
"ELEV_SC",
"CENTRAL_FQ_DN",
"FSL_DN",
"POLAR",
"DIAMETER",
"EFFICIENCY",
"POLAR_TILT_ANGLE",
"PROPAG_DN",
"BEAM_TX_CENTER_AZ_ANT",
"BEAM_TX_CENTER_EL_ANT",
"BEAM_TX_ANT_DIAM",
"BEAM_TX_TYPE",
"MAX_GAIN_TX",
"BEAM_TX_THETA_3DB",
"SAT_GAIN_TX",
"IBO",
"AMP_SAT",
"OBO",
"SAT_EIRP","CSIM0","CSN0_DN","CSI0_DN","GPT"):
        for key in vsat.keys():
            vsat[key].append(row["_extra"][key])
    #SAT
    for row in dbLinkBudget(dbLinkBudget.Earth_coord_GW.Job_ID == request.args(0)).iterselect(groupby='SAT_ID'): #this looks for the different types of Satellite referred to in gateway Earth_coord
        rowt = dbLinkBudget(dbLinkBudget.SAT.SAT_ID == row['SAT_ID']).iterselect("SAT_ID", "NADIR_LON", "NADIR_LAT", "DISTANCE", "INCLINATION_ANGLE", "FOV_RADIUS", "FLAG_ASC_DESC", "INTERF_FLAG", "ROLL",
                                                                                              "PITCH", "YAW", "PAYLOAD_ID", "NADIR_X_ECEF", "NADIR_Y_ECEF", "NADIR_Z_ECEF", "SAT_POS_X_ECEF", "SAT_POS_Y_ECEF", "SAT_POS_Z_ECEF",
                                                                                              "NORMAL_VECT_X", "NORMAL_VECT_Y", "NORMAL_VECT_Z").first().as_dict()

        sat = OrderedDict.fromkeys(rowt["_extra"])
        for key in sat.keys():
            sat[key] = []
        for row in dbLinkBudget(dbLinkBudget.SAT.SAT_ID == row['SAT_ID']).iterselect("SAT_ID", "NADIR_LON", "NADIR_LAT", "DISTANCE", "INCLINATION_ANGLE", "FOV_RADIUS", "FLAG_ASC_DESC", "INTERF_FLAG", "ROLL",
                                                                                              "PITCH", "YAW", "PAYLOAD_ID", "NADIR_X_ECEF", "NADIR_Y_ECEF", "NADIR_Z_ECEF", "SAT_POS_X_ECEF", "SAT_POS_Y_ECEF", "SAT_POS_Z_ECEF",
                                                                                              "NORMAL_VECT_X", "NORMAL_VECT_Y", "NORMAL_VECT_Z"):
            for key in sat.keys():
                sat[key].append(row["_extra"][key])
    #TRSP
    for row in dbLinkBudget(dbLinkBudget.Earth_coord_GW.Job_ID == request.args(0)).iterselect(groupby='PAYLOAD_ID'): #this looks for the different types of Satellite referred to in gateway Earth_coord
        rowt = dbLinkBudget(dbLinkBudget.TRSP.PAYLOAD_ID == row['PAYLOAD_ID']).iterselect("FWD_RTN_FLAG", "PAYLOAD_ID", "TRSP_ID", "SYS_TEMP", "CENTRAL_FQ_UP", "BANDWIDTH", "CENTRAL_FQ_DN","AMP_SAT", "IBO", "BEAM_RX_ID",
                                                                                 "BEAM_RX_TYPE", "BEAM_RX_CENTER_AZ_ANT", "BEAM_RX_CENTER_EL_ANT", "BEAM_RX_ANT_DIAM", "BEAM_RX_THETA_3DB", "BEAM_RX_EFF", "BEAM_RX_RADIUS",
                                                                                 "BEAM_TX_ID", "BEAM_TX_TYPE", "BEAM_TX_CENTER_AZ_ANT", "BEAM_TX_CENTER_EL_ANT", "BEAM_TX_ANT_DIAM", "BEAM_TX_THETA_3DB",
                                                                                 "BEAM_TX_EFF", "BEAM_TX_RADIUS", "MAX_GAIN_TX").first().as_dict()

        trsp = OrderedDict.fromkeys(rowt["_extra"])
        for key in trsp.keys():
            trsp[key] = []
        for row in dbLinkBudget(dbLinkBudget.TRSP.PAYLOAD_ID == row['PAYLOAD_ID']).iterselect("FWD_RTN_FLAG", "PAYLOAD_ID", "TRSP_ID", "SYS_TEMP", "CENTRAL_FQ_UP",
                                                                                     "BANDWIDTH", "CENTRAL_FQ_DN","AMP_SAT", "IBO", "BEAM_RX_ID", "BEAM_RX_TYPE",
                                                                                     "BEAM_RX_CENTER_AZ_ANT", "BEAM_RX_CENTER_EL_ANT", "BEAM_RX_ANT_DIAM",
                                                                                     "BEAM_RX_THETA_3DB", "BEAM_RX_EFF", "BEAM_RX_RADIUS", "BEAM_TX_ID", "BEAM_TX_TYPE",
                                                                                     "BEAM_TX_CENTER_AZ_ANT", "BEAM_TX_CENTER_EL_ANT", "BEAM_TX_ANT_DIAM", "BEAM_TX_THETA_3DB",
                                                                                     "BEAM_TX_EFF", "BEAM_TX_RADIUS", "MAX_GAIN_TX"):
            for key in trsp.keys():
                trsp[key].append(row["_extra"][key])

    filename = "Output file " + request.args(0) + ".xlsx"
    filepath = os.path.join(request.folder, 'uploads', filename) # TODO: look at maybe use .retrieve() here
    create_saving_worksheet(filepath, sat, "SAT", trsp, "TRSP", vsat, "EARTH_coord_VSAT")
    stream = open(filepath, 'rb')
    dbLinkBudget(dbLinkBudget.Job.id == request.args(0)).update(
        processed_file=dbLinkBudget.Job.processed_file.store(stream, filepath))
    os.remove(filepath)
    redirect(URL('download', args=dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).processed_file))


def run():
    """
    This runs the processing of the excel file.
    Currently asks which propagation library is being used.
    Adds EIRP values (in fact it outputs temperature at the moment)
    Updates 'processed' checkbox.

    Returns:
        Refreshes the update page

    """

    file = dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).file_up  # Find uploaded file
    job_id = dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).id
    [SAT_dict, TRSP_dict, VSAT_dict, EARTH_COORD_GW_dict, GW_dict, EARTH_COORD_VSAT_dict,
     display_dict_VSAT] = load_objects_from_xl(os.path.join(request.folder, 'uploads', file))
    if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).sat_geo_params == True:
    #-----------------  1/ Compute SAT geometric params ------------------
        SAT_dict, nadir_ecef, pos_ecef, normal_vector = compute_sat_params(SAT_dict, True)
    if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).sat_fov == True:
        values =  display_sat_field_of_views_for_cesium(nadir_ecef, pos_ecef, normal_vector, \
                                                     SAT_dict['FOV_RADIUS']*np.pi/180, \
                                                     SAT_dict['ROLL']*np.pi/180, \
                                                     SAT_dict['PITCH']*np.pi/180, \
                                                     SAT_dict['YAW']*np.pi/180)
        lat = np.array([])
        lon = np.array([])
        count = np.array([])
        for i in np.arange(0,np.size(values,0)/2):
            lon = np.append(lon, values[2*i,:])
            lat = np.append(lat, values[2*i+1,:])
            count = np.append(count, np.full(len(values[2*i,:]), i+1))
            sat_fov_dict = {'SAT_ID':count, 'LON':lon, 'LAT':lat}
            read_array_to_db(dbLinkBudget.SAT_FOV, sat_fov_dict, job_id)

    #----------------- 2/ Assign sat to each point of coverage -----------
    if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).points2trsp == True:
        if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).simulator_mode == 'FWD':
            EARTH_COORD_VSAT_dict = compute_transponder_assignment(EARTH_COORD_VSAT_dict, SAT_dict, TRSP_dict, 'FWD', 'DN')
        elif dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).simulator_mode == 'RTN':
            EARTH_COORD_VSAT_dict = compute_transponder_assignment(EARTH_COORD_VSAT_dict, SAT_dict, TRSP_dict, 'RTN', 'UP')
    if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).gw2trsp == True:
        if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).simulator_mode == 'FWD':
            EARTH_COORD_GW_dict = compute_transponder_assignment(EARTH_COORD_GW_dict, SAT_dict, TRSP_dict, 'FWD', 'UP') #BUG this should be EARTH_COORD_GW_dict
        elif dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).simulator_mode == 'RTN':
            EARTH_COORD_GW_dict = compute_transponder_assignment(EARTH_COORD_GW_dict, SAT_dict, TRSP_dict, 'RTN', 'DN') #BUG this should be EARTH_COORD_GW_dict
    #----------------- 3/ Compute RX/TX COV geometric params -------------------
    if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).comp_point_cover == True:
        EARTH_COORD_VSAT_dict = compute_coverage_points_geo_params(SAT_dict, EARTH_COORD_VSAT_dict)
    if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).comp_gw_cover == True:
        EARTH_COORD_GW_dict = compute_coverage_points_geo_params(SAT_dict, EARTH_COORD_GW_dict)
    #----------------- 4/ Compute propag params -------------------
    if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).propa_feeder_link == True:
        if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).simulator_mode == 'FWD':
            EARTH_COORD_GW_dict = compute_lkb_propag_params(EARTH_COORD_GW_dict, SAT_dict, TRSP_dict, GW_dict, 'UP', True, 'FWD')  #BUG this should be EARTH_COORD_GW_dict
        if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).simulator_mode == 'RTN':
             EARTH_COORD_GW_dict = compute_lkb_propag_params(EARTH_COORD_GW_dict, SAT_dict, TRSP_dict, GW_dict, 'DN', True, 'RTN')  #BUG this should be EARTH_COORD_GW_dict
    if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).propa_user_link == True:
        if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).simulator_mode == 'FWD':
            EARTH_COORD_VSAT_dict = compute_lkb_propag_params(EARTH_COORD_VSAT_dict, SAT_dict, TRSP_dict, VSAT_dict, 'DN', True, 'FWD')
        if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).simulator_mode == 'RTN':
            EARTH_COORD_VSAT_dict = compute_lkb_propag_params(EARTH_COORD_VSAT_dict, SAT_dict, TRSP_dict, VSAT_dict, 'UP', True, 'RTN')
    #----------------- 5/ Compute satellite perfos -------------------
    if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).sat_up_perf == True:
        EARTH_COORD_VSAT_dict = compute_satellite_perfos(EARTH_COORD_VSAT_dict, TRSP_dict, 'UP')
    if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).sat_dwn_perf == True:
        EARTH_COORD_VSAT_dict = compute_satellite_perfos(EARTH_COORD_VSAT_dict, TRSP_dict, 'DN')
    #if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).comp_link_budget == True: #  NOT YET IMPLEMENTED IN THE LIBRARY
    #    if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).simulator_mode == 'FWD':
    #        EARTH_COORD_VSAT_dict = compute_lkb_perfos(EARTH_COORD_GW_dict,EARTH_COORD_VSAT_dict, GW_dict, VSAT_dict, 'FWD', 'disregard', 'disregard', 'disregard', 'compute', 'disregard')
    #       EARTH_COORD_VSAT_dict = compute_lkb_perfos(EARTH_COORD_GW_dict,EARTH_COORD_VSAT_dict, GW_dict, VSAT_dict, 'FWD', csn0_up_flag, \
    #                                                                           csi0_up_flag, \
    #                                                                           csim0_flag, \
    #                                                                           csn0_dn_flag, \
    #                                                                           csi0_dn_flag):

    #### This is get transponder FOV circles
    if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).trsp_fov == True:
        for SAT_ID in map(int,SAT_dict['SAT_ID']):
            beam_centers_lonlat, beam_contour_ll = display_2D_sat_and_beams_for_cesium(SAT_ID, SAT_dict['SAT_ID'], SAT_dict['PAYLOAD_ID'], nadir_ecef, pos_ecef, normal_vector, \
                                TRSP_dict['PAYLOAD_ID'], TRSP_dict['BEAM_TX_CENTER_AZ_ANT'], TRSP_dict['BEAM_TX_CENTER_EL_ANT'], TRSP_dict['BEAM_TX_RADIUS'])
            lat = np.array([])
            lon = np.array([])
            count = np.array([])
            SAT_IDs = np.array([])
            for i in np.arange(0,np.size( beam_contour_ll,0)/2):
                lon = np.append(lon, beam_contour_ll[2*i,:])
                lat = np.append(lat, beam_contour_ll[2*i+1,:])
                count = np.append(count, np.full(len(beam_contour_ll[2*i,:]), i+1))
                SAT_IDs = np.append(SAT_IDs, np.full(len(beam_contour_ll[2*i,:]), SAT_ID))
                trsp_fov_dict = {'SAT_ID': SAT_IDs,'TRSP_ID':count,'LON':lon, 'LAT':lat}
                read_array_to_db(dbLinkBudget.TRSP_FOV, trsp_fov_dict, job_id)
    read_array_to_db(dbLinkBudget.TRSP, TRSP_dict) #at the moment these write to new lines
    read_array_to_db(dbLinkBudget.SAT, SAT_dict)
    read_array_to_db(dbLinkBudget.EARTH_coord_VSAT, EARTH_COORD_VSAT_dict, job_id)
    read_array_to_db(dbLinkBudget.Earth_coord_GW, EARTH_COORD_GW_dict, job_id)
    dbLinkBudget(dbLinkBudget.Job.id == request.args(0)).update(processed=True)
    redirect(URL('launch', args=request.args(0)))


def cesium():
    """    Cesium viewing page cesium.html    """
    return dict(a=1)


def copy(): # TODO: Add all of the new fields to this list
    """
    Function for a copy button on update.html.
    It copies the currently viewed data entry to a new row and renames it _copy

    """
    a = dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0))
    filename, stream = dbLinkBudget.Job.file_up.retrieve(a.file_up)
    dbLinkBudget.Job.insert(job_name= '%s_copy' % (a.job_name),
                            Date = request.now,
                            file_up = dbLinkBudget.Job.file_up.store(stream, filename), #this needs to be renamed
                            simulator_mode = a.simulator_mode,
                            sat_geo_params = a.sat_geo_params,
                            points2trsp = a.points2trsp,
                            gw2trsp = a.gw2trsp,
                            comp_point_cover = a.comp_point_cover,
                            comp_gw_cover = a.comp_gw_cover,
                            propa_feeder_link = a.propa_feeder_link,
                            propa_user_link = a.propa_user_link,
                            sat_up_perf = a.sat_up_perf,
                            sat_dwn_perf = a.sat_dwn_perf,
                            comp_link_budget = a.comp_link_budget,
                            description = a.description,
                            processed = a.processed)
    session.flash = "%s has been copied" % (request.args(0))
    redirect(URL('select'))

def maxmin(dbtablecol, option):
    """
    Function to get the maximum value of a column.

    Usage:
    maxmin(dbLinkBudget.EARTH_coord_VSAT.SAT_EIRP, 'min')
    """
    if option == 'max':
        field = dbtablecol.max()
    if option == 'min':
        field = dbtablecol.min()
    return dbLinkBudget(dbtablecol).select(field)

def testmax():
    return maxmin(dbLinkBudget.EARTH_coord_VSAT.SAT_EIRP, 'min')

def VSATcoverage(lat, lon, npoints, distance):
    """
    Produces 2 arrays

    Usage example:
    VSATcoverage(-90,0,300,.2)
    """
    sidelength = np.floor(np.sqrt(npoints))
    lonarray_calc = np.arange(lon - (distance * sidelength / 2), lon + (distance * sidelength / 2), distance)
    lonarray = np.empty([0, 100])
    latarray = np.empty([0, 100])
    for i in lonarray_calc:
        if 360 > i > 180:
            i = -180 + i % 180
            lonarray = np.append(lonarray, i)
        elif -180 > i > -360:
            i = i % 180
            lonarray = np.append(lonarray, i)
        else:
            lonarray = np.append(lonarray, i)
    latarray_calc = np.arange(lat - (distance * sidelength / 2), lat + (distance * sidelength / 2), distance)
    for i in latarray_calc:
        if i > 90 or i < -90:
            i = 0
            latarray = np.append(latarray, i)
        else:
            latarray = np.append(latarray, i)
    latfull = np.repeat(latarray, sidelength)
    lonfull = np.tile(lonarray, sidelength)
    EARTH_COORD_VSAT_dict = {'LON': lonfull, 'LAT': latfull}
    return EARTH_COORD_VSAT_dict

def testthis():
    return VSATcoverage(-90.,0.,300.,0.2) #you need to convert the output from a np array to something else to show it in a browser. Or do eg lonarray[3]

def get_geojson():
    """
    Function to get the coordinates into a GeoJSON format
    This adds the lat and longitude for the User Terminals
    Called in cesium.html

    Returns:
        object: GeoJSON
    """
    rows = dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.Job_ID == request.args(0)).iterselect() # TODO : test if iterselect is better than regular select, time and memory resources.
    features = [{"type": "Feature",
                 "geometry": {
                     "type": "Point",
                     "coordinates": [r[dbLinkBudget.EARTH_coord_VSAT.LON], r[dbLinkBudget.EARTH_coord_VSAT.LAT]]
                 },
                 "properties": {
                     "title": [str(r[dbLinkBudget.EARTH_coord_VSAT.VSAT_ID])],
                     "Job ID": r[dbLinkBudget.EARTH_coord_VSAT.Job_ID],
                     "EIRP": r[dbLinkBudget.EARTH_coord_VSAT.SAT_EIRP],
                     "ELEVATION": r[dbLinkBudget.EARTH_coord_VSAT.ELEVATION],
                     "SAT_GPT": r[dbLinkBudget.EARTH_coord_VSAT.SAT_GPT],
                     "Lat": r[dbLinkBudget.EARTH_coord_VSAT.LAT],
                     "Lon": r[dbLinkBudget.EARTH_coord_VSAT.LON],
                 }
                 } for r in rows if r[dbLinkBudget.EARTH_coord_VSAT.ELEVATION]]  # TODO : Extend to include more information form database #hacky way to ignore NONEs
    return response.json({"type": "FeatureCollection", 'features': features})


def get_geojson_gw():
    """
    Function to get the coordinates into a GeoJSON format
    This adds the lat and longitudes for the gateways
    Called in cesium.html

    Returns:
        object: GeoJSON
    """
    rows = dbLinkBudget(dbLinkBudget.Earth_coord_GW.Job_ID == request.args(0)).iterselect()

    features = [{"type": "Feature",
                 "geometry": {
                     "type": "Point",
                     "coordinates": [r[dbLinkBudget.Earth_coord_GW.LON], r[dbLinkBudget.Earth_coord_GW.LAT]]
                 },
                 "properties": {
                     "title": "Gateway",
                     "Job ID": r[dbLinkBudget.Earth_coord_GW.Job_ID],
                     "Gateway ID": r[dbLinkBudget.Earth_coord_GW.GW_ID],
                     "EIRP Max": dbLinkBudget.Gateway(
                         dbLinkBudget.Gateway.GW_ID == r[dbLinkBudget.Earth_coord_GW.GW_ID]).EIRP_MAX,
                     "Bandwidth": dbLinkBudget.Gateway(
                         dbLinkBudget.Gateway.GW_ID == r[dbLinkBudget.Earth_coord_GW.GW_ID]).BANDWIDTH,
                     "Diameter": dbLinkBudget.Gateway(
                         dbLinkBudget.Gateway.GW_ID == r[dbLinkBudget.Earth_coord_GW.GW_ID]).DIAMETER,
                     "Lat": r[dbLinkBudget.Earth_coord_GW.LAT],
                     "Lon": r[dbLinkBudget.Earth_coord_GW.LON],
                 }
                 } for r in rows]
    return response.json({"type": "FeatureCollection", 'features': features})

def get_geojson_sat():
    """
    Function to get the coordinates into a GeoJSON format
    This adds the lat and longitudes for the SAT
    Called in cesium.html

    Returns:
        object: GeoJSON
    """
    rows = dbLinkBudget(dbLinkBudget.Earth_coord_GW.Job_ID == request.args(0)).iterselect()

    features = [{"type": "Feature",
                 "geometry": {
                     "type": "Point",
                     "coordinates": [dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).NADIR_LON, dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).NADIR_LAT, (dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).DISTANCE)*1000]
                 },
                 "properties": {
                     "title": "SAT",
                     "Height": dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).DISTANCE,
                     "SAT ID": r[dbLinkBudget.Earth_coord_GW.SAT_ID],
                     "Job ID": r[dbLinkBudget.Earth_coord_GW.Job_ID],
                     "FOV Radius": dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).FOV_RADIUS,
                     "Payload ID": dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).PAYLOAD_ID,
                     "Lat": dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).NADIR_LAT,
                     "Lon": dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).NADIR_LON,
#                     "NADIR_LON": dbLinkBudget.Gateway(dbLinkBudget.Gateway.GW_ID == r[dbLinkBudget.Earth_coord_GW.GW_ID]).EIRP_MAX,
#                     "Bandwidth": dbLinkBudget.Gateway(
#                         dbLinkBudget.Gateway.GW_ID == r[dbLinkBudget.Earth_coord_GW.GW_ID]).BANDWIDTH,
#                     "Diameter": dbLinkBudget.Gateway(
#                         dbLinkBudget.Gateway.GW_ID == r[dbLinkBudget.Earth_coord_GW.GW_ID]).DIAMETER
                 }
                 } for r in rows]
    return response.json({"type": "FeatureCollection", 'features': features})

def get_geojson_FOV():
    """
    Function to get the coordinates into a GeoJSON format
    This adds the lat and longitudes for the SAT
    Called in cesium.html

    Returns:
        object: GeoJSON
    """
    rows = dbLinkBudget(dbLinkBudget.Earth_coord_GW.Job_ID == request.args(0)).iterselect()

    features = [{"type": "Feature",
                 "geometry": {
                     "type": "Point",
                     "coordinates": [dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).NADIR_LON, dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).NADIR_LAT, (dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).DISTANCE)*1000/2]
                 },
                 "properties": {
                     "title": "SAT",
                     "Height": dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).DISTANCE,
                     "SAT ID": r[dbLinkBudget.Earth_coord_GW.SAT_ID],
                     "Job ID": r[dbLinkBudget.Earth_coord_GW.Job_ID],
                     "FOVBottomRadius": (dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).DISTANCE)*1000*np.tan((np.pi/180)*(dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).FOV_RADIUS)),
                     "Payload ID": dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).PAYLOAD_ID,
                     "Lat": dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).NADIR_LAT,
                     "Lon": dbLinkBudget.SAT(dbLinkBudget.SAT.SAT_ID == r[dbLinkBudget.Earth_coord_GW.SAT_ID]).NADIR_LON,
                 }
                 } for r in rows]
    return response.json({"type": "FeatureCollection", 'features': features})


def get_geojson_FOV_CIRCLE():
    """
    Function to get the coordinates into a GeoJSON format
    This adds the lat and longitudes for the SAT
    Called in cesium.html

    Returns:
        object: GeoJSON
    """
    rows = dbLinkBudget((dbLinkBudget.SAT_FOV.Job_ID == request.args(0))).iterselect()
    coordinates = {}

    for row in rows:
        if row[dbLinkBudget.SAT_FOV.SAT_ID] not in coordinates.keys() :
              coordinates[row[dbLinkBudget.SAT_FOV.SAT_ID]] = []
        coordinates[row[dbLinkBudget.SAT_FOV.SAT_ID]].append([row[dbLinkBudget.SAT_FOV.LON], row[dbLinkBudget.SAT_FOV.LAT]])

    features = [{"type": "Feature",
                  "geometry": {
                  "type": "LineString",
                   "coordinates": coordinates[i]
                  },
                 "properties": {
                 "title": "SAT",
                 "SAT ID": i}
               } for i in coordinates.keys()]

    return response.json({"type": "FeatureCollection", 'features': features})

def get_geojson_TRSP_FOV_CIRCLE():
    """
    Function to get the coordinates into a GeoJSON format
    This adds the lat and longitudes for the SAT
    Called in cesium.html

    Returns:
        object: GeoJSON
    """
    rows = dbLinkBudget((dbLinkBudget.TRSP_FOV.Job_ID == request.args(0))&(dbLinkBudget.TRSP_FOV.TRSP_ID > 0)).iterselect()
    coordinates = {}

    for row in rows:
        if (row[dbLinkBudget.TRSP_FOV.SAT_ID],row[dbLinkBudget.TRSP_FOV.TRSP_ID]) not in coordinates.keys() :
              coordinates[row[dbLinkBudget.TRSP_FOV.SAT_ID],row[dbLinkBudget.TRSP_FOV.TRSP_ID]] = []
        coordinates[row[dbLinkBudget.TRSP_FOV.SAT_ID],row[dbLinkBudget.TRSP_FOV.TRSP_ID]].append([row[dbLinkBudget.TRSP_FOV.LON], row[dbLinkBudget.TRSP_FOV.LAT]])

    features = [{"type": "Feature",
                  "geometry": {
                  "type": "LineString",
                   "coordinates": coordinates[i]
                  },
                 "properties": {
                 "title": "TRSP",
                "SAT ID": i[0],
                 "TRSP ID": i[1]}
               } for i in coordinates.keys()]

    return response.json({"type": "FeatureCollection", 'features': features})


def display_2D_sat_and_beams(az_beam_centers, elev_beam_centers, nadir_ecef, sat_pos_ecef, normal_vector, beam_radius):
    '''
    display nadir and beam centers and contours of ONE satellite

    '''
    # duplicate nadir as many times as number of beams (to allow for vectorized calculations)
    nadir_ecef_disp = np.outer(nadir_ecef, np.ones(np.size(az_beam_centers)))
    pos_disp = np.outer(sat_pos_ecef, np.ones(np.size(az_beam_centers)))
    normal_vector_disp = np.outer(normal_vector, np.ones(np.size(az_beam_centers)))

    # compute ecef coord of beam centers
    points_ecef = compute_az_elev_to_ecef(np.array([az_beam_centers,elev_beam_centers]), \
                                nadir_ecef_disp, \
                                pos_disp, \
                                normal_vector_disp \
                                )

    # convert to lonlat
    beam_centers_lonlat = ecef2ll_geod(points_ecef)


    # for each beam
    beam_contour_ll = np.array([[np.nan,np.nan]]).T
    for i in np.arange(0, np.size(az_beam_centers)):
        #compute contour
        mv = compute_beam_contour(np.array([az_beam_centers,elev_beam_centers])[:,i], beam_radius[i]) #6.7

        # convert contour in ecef and then lonlat coord
        nadir_ecef_disp = np.outer(nadir_ecef, np.ones(np.size(mv,1)))
        pos_disp = np.outer(sat_pos_ecef, np.ones(np.size(mv,1)))
        normal_vector_disp = np.outer(normal_vector, np.ones(np.size(mv,1)))

        points_ecef = compute_az_elev_to_ecef(mv, \
                                nadir_ecef_disp, \
                                pos_disp, \
                                normal_vector_disp \
                                )
        mv_ll = ecef2ll_geod(points_ecef)

        #save contour with putting a "nan" between each contour
        beam_contour_ll = np.append(beam_contour_ll, np.array([[np.nan,np.nan]]).T, axis=1)
        beam_contour_ll = np.append(beam_contour_ll, mv_ll, axis=1)


    return beam_centers_lonlat, beam_contour_ll

#
# @request.restful()
# def api():
#
#     def GET(*args, **vars):
#         return dict()
#
#     def POST(*args, **vars):
#         return dict()
#
#     def PUT(*args, **vars):
#         return dict()
#
#     def DELETE(*args, **vars):
#         return dict()
#
#     return locals()

@request.restful()
def api():
    response.view = 'generic.'+request.extension
    def GET(*args,**vars):
        patterns = 'auto'
        parser = dbLinkBudget.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            return dict(content=parser.response)
        else:
            raise HTTP(parser.status,parser.error)
    # def POST(table_name,**vars):
    #     return dbLinkBudget[Job].validate_and_insert(**vars)
    # def PUT(table_name,record_id,**vars):
    #     return dbLinkBudget(dbLinkBudget[Job]._id==record_id).update(**vars)
    # def DELETE(table_name,record_id):
    #     return dbLinkBudget(dbLinkBudget[Job]._id==record_id).delete()
    return dict(GET=GET)
