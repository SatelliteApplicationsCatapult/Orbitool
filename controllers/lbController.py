# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is the Link Budget Controller
# -------------------------------------------------------------------------
import json
from datetime import datetime

import logging
logger = logging.getLogger("web2py.app.myweb2pyapplication")
logger.setLevel(logging.DEBUG)


from dbhandling import*
from excelHandling import *
from gluon import *
from lib_lkb.compute_high_level_func import *
from lib_lkb.display_func import *
from collections import OrderedDict

import platform

if platform.system() is 'Windows':
    from lib_lkb.propa_func_windows import *
elif platform.system() is 'Linux':
    from lib_lkb.propa_func_linux import *

response.title = 'Orbitool'


def index():
    """ Input form """
    # TODO: Think about adding drag and drop plugin
    # TODO : separate the form
    session.job = ""
    record = dbLinkBudget.Job(request.args(0))
    dbLinkBudget.Job.Date.readable = False
    form = SQLFORM(dbLinkBudget.Job, record, deletable=True,
                   upload=URL('download'), formstyle='table3cols')
    if form.process().accepted:
        dbLinkBudget.Calculate.insert(Job_ID=form.vars.id)
        session.flash = "Scenario %s - %s has been uploaded!" % (
            form.vars.id, form.vars.job_name)
        session.job = form.vars.id
        add_excel_2_db()
    elif form.errors:
        session.flash = "%s - %s has FAILED" % (
            form.vars.id, form.vars.job_name)
    return dict(form=form)


def about():
    """ About page """
    return dict(message=T('About'))


def select():
    """  Page which renders a JQuery Datatable to let you select entries  """
    import json
    job = json.dumps(dbLinkBudget(dbLinkBudget.Job).select().as_list(),
                     default=json_serial)  # Formatting need to interface with JQuery Datatables
    return dict(job=XML(job))


def add_excel_2_db():
    """
    Function used to insert excel dictionary into database

    """
    fileName = dbLinkBudget.Job(
        dbLinkBudget.Job.id == session.job).file_up  # Find uploaded file
    job_id = dbLinkBudget.Job(dbLinkBudget.Job.id == session.job).id
    excel_info = load_objects_from_xl(
        os.path.join(request.folder, 'uploads', fileName))
    write_dict_to_table(dbLinkBudget.SAT, excel_info[0], job_id, dbLinkBudget)
    write_dict_to_table(dbLinkBudget.TRSP, excel_info[1], job_id, dbLinkBudget)
    write_dict_to_table(dbLinkBudget.VSAT, excel_info[2], job_id, dbLinkBudget)
    write_dict_to_table(dbLinkBudget.Earth_coord_GW,
                        excel_info[3], job_id, dbLinkBudget)
    write_dict_to_table(dbLinkBudget.Gateway,
                        excel_info[4], job_id, dbLinkBudget)
    write_dict_to_table(dbLinkBudget.EARTH_coord_VSAT,
                        excel_info[5], job_id, dbLinkBudget)

    redirect(URL('preview', args=job_id))


def preview():
    # SQL FORM
    """
    This form is to determine which calculations to perform
    """
    job_id = request.args(0)
    dbLinkBudget.Calculate.processed.readable = False
    dbLinkBudget.Calculate.processed.writable = False
    dbLinkBudget.Calculate.Job_ID.writable = False

    record = dbLinkBudget.Calculate(dbLinkBudget.Calculate.Job_ID == job_id)
    form = SQLFORM(dbLinkBudget.Calculate, record, showid=False,
                   formstyle='table3cols', submit_button='')
    if form.accepts(request, session):
        response.flash = 'form accepted'
        redirect(URL('run', args=request.args(0)))
    elif form.errors:
        response.flash = 'form has errors'
    return dict(form=form)


def delete_row_editablegrid():
    """
    Function to delete a row in the preview page from the database
    """
    temparray = json.loads(request.post_vars.array)
    print temparray["rowid"]
    if temparray["table"] == "SAT":
        dbLinkBudget(dbLinkBudget.SAT.id == temparray["rowid"]).delete()
        print "delete successfull"
    if temparray["table"] == "GW":
        dbLinkBudget(dbLinkBudget.Gateway.id == temparray["rowid"]).delete()
        print "delete successfull"
    if temparray["table"] == "TRSP":
        dbLinkBudget(dbLinkBudget.TRSP.id == temparray["rowid"]).delete()
        print "delete successfull"


def copy():
    """
    Copy function for eitablegrid on the preview page
    :return:
    """
    data = json.loads(request.post_vars.array)
    if data['table'] == 'SAT':
        row = dbLinkBudget(dbLinkBudget.SAT.id == data['rowid']).select(dbLinkBudget.SAT.ALL).first()
        dbLinkBudget.SAT.insert(**dbLinkBudget.SAT._filter_fields(row))
        print "copy successfull sat"
    if data['table'] == 'TRSP':
        row = dbLinkBudget(dbLinkBudget.TRSP.id == data['rowid']).select(dbLinkBudget.TRSP.ALL).first()
        dbLinkBudget.TRSP.insert(**dbLinkBudget.TRSP._filter_fields(row))
        print "copy successfull trsp"
    if data['table'] == 'GW':
        print data['rowid']
        row = dbLinkBudget(dbLinkBudget.Earth_coord_GW.id == data['rowid']).select(dbLinkBudget.Earth_coord_GW.ALL).first()
        print row
        dbLinkBudget.Earth_coord_GW.insert(**dbLinkBudget.Earth_coord_GW._filter_fields(row))
        print "copy successfull gw"


def ajax_to_db():
    """
    read from editableGrid
    ajax and write to the database tables
    """
    temparray = json.loads(request.post_vars.array)
    if temparray["table"] == "SAT":
        # Get the row to insert into
        row = dbLinkBudget(dbLinkBudget.SAT.id ==
                           temparray["rowid"]["rowId"]).select().first()
        if temparray["columnname"] == "SAT_ID":
            row.update_record(SAT_ID=temparray["value"])
        elif temparray["columnname"] == "NADIR_LON":
            row.update_record(NADIR_LON=temparray["value"])
        elif temparray["columnname"] == "NADIR_LAT":
            row.update_record(NADIR_LAT=temparray["value"])
        elif temparray["columnname"] == "DISTANCE":
            row.update_record(DISTANCE=temparray["value"])
        elif temparray["columnname"] == "FOV_RADIUS":
            row.update_record(FOV_RADIUS=temparray["value"])
        elif temparray["columnname"] == "INCLINATION_ANGLE":
            row.update_record(INCLINATION_ANGLE=temparray["value"])
        elif temparray["columnname"] == "FLAG_ASC_DESC":
            row.update_record(FLAG_ASC_DESC=temparray["value"])
        elif temparray["columnname"] == "ROLL":
            row.update_record(ROLL=temparray["value"])
        elif temparray["columnname"] == "PITCH":
            row.update_record(PITCH=temparray["value"])
        elif temparray["columnname"] == "YAW":
            row.update_record(YAW=temparray["value"])
        else:
            raise Exception('There was a problem writing to the SAT datatable')
    if temparray["table"] == "TRSP":
        # Get the row to insert into
        row = dbLinkBudget(dbLinkBudget.TRSP.id ==
                           temparray["rowid"]["rowId"]).select().first()
        if temparray["columnname"] == "TRSP_ID":
            row.update_record(TRSP_ID=temparray["value"])
        elif temparray["columnname"] == "PAYLOAD_ID":
            row.update_record(PAYLOAD_ID=temparray["value"])
        elif temparray["columnname"] == "BEAM_RX_CENTER_X_ANT":
            row.update_record(BEAM_RX_CENTER_X_ANT=temparray["value"])
        elif temparray["columnname"] == "BEAM_RX_CENTER_Y_ANT":
            row.update_record(BEAM_RX_CENTER_Y_ANT=temparray["value"])
        elif temparray["columnname"] == "BEAM_RX_CENTER_Z_ANT":
            row.update_record(BEAM_RX_CENTER_Z_ANT=temparray["value"])
        elif temparray["columnname"] == "BEAM_RX_RADIUS":
            row.update_record(BEAM_RX_RADIUS=temparray["value"])
        elif temparray["columnname"] == "BEAM_TX_CENTER_X_ANT":
            row.update_record(BEAM_TX_CENTER_X_ANT=temparray["value"])
        elif temparray["columnname"] == "BEAM_TX_CENTER_Y_ANT":
            row.update_record(BEAM_TX_CENTER_Y_ANT=temparray["value"])
        elif temparray["columnname"] == "BEAM_TX_CENTER_Z_ANT":
            row.update_record(BEAM_TX_CENTER_Z_ANT=temparray["value"])
        elif temparray["columnname"] == "BEAM_TX_RADIUS":
            row.update_record(BEAM_TX_RADIUS=temparray["value"])
        else:
            raise Exception(
                'There was a problem writing to the TRSP datatable')
    if temparray["table"] == "GW":
        # Get the row to insert into
        row = dbLinkBudget(dbLinkBudget.Earth_coord_GW.id ==
                           temparray["rowid"]["rowId"]).select().first()
        if temparray["columnname"] == "LON":
            row.update_record(LON=temparray["value"])
        elif temparray["columnname"] == "LAT":
            row.update_record(LAT=temparray["value"])
        elif temparray["columnname"] == "ALT":
            row.update_record(ALT=temparray["value"])
        elif temparray["columnname"] == "GW_ID":
            row.update_record(GW_ID=temparray["value"])
        else:
            raise Exception(
                'There was a problem writing to the TRSP datatable')


def transponder_JSON():
    """
    Returns a JSON to be read by the editablegrid
    """
    job_id = request.args(0)
    trsp_table = dbLinkBudget.TRSP
    rows = dbLinkBudget(trsp_table.Job_ID == request.args(0)).select(trsp_table.id, trsp_table.PAYLOAD_ID, trsp_table.TRSP_ID,
                                                                     trsp_table.BEAM_RX_CENTER_X_ANT, trsp_table.BEAM_RX_CENTER_Y_ANT, trsp_table.BEAM_RX_CENTER_Z_ANT, trsp_table.BEAM_RX_RADIUS,                                                                trsp_table.BEAM_RX_RADIUS, trsp_table.BEAM_TX_CENTER_X_ANT,
                                                                     trsp_table.BEAM_TX_CENTER_X_ANT, trsp_table.BEAM_TX_CENTER_Y_ANT, trsp_table.BEAM_TX_CENTER_Z_ANT, trsp_table.BEAM_TX_RADIUS)

    metadata = [
        {"name": "PAYLOAD_ID", "label": "Payload ID",
            "datatype": "double", "editable": "true"},
        {"name": "TRSP_ID", "label": "Trsp ID",
            "datatype": "double", "editable": "true"},
        {"name": "BEAM_RX_CENTER_X_ANT", "label": "RX Centr. X ANT",
            "datatype": "double(, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "BEAM_RX_CENTER_Y_ANT", "label": "RX Centr. Y ANT",
            "datatype": "double(, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "BEAM_RX_CENTER_Z_ANT", "label": "RX Centr. Z ANT",
         "datatype": "double(, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "BEAM_RX_RADIUS", "label": "RX Radius",
            "datatype": "double(, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "BEAM_TX_CENTER_X_ANT", "label": "TX Centr. X ANT",
            "datatype": "double(, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "BEAM_TX_CENTER_Y_ANT", "label": "TX Centr. Y ANT",
            "datatype": "double(, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "BEAM_TX_CENTER_Z_ANT", "label": "TX Centr. Z ANT",
         "datatype": "double(, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "BEAM_TX_RADIUS", "label": "TX Radius",
            "datatype": "double(deg, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "action", "label": "", "datatype": "html", "editable": 'false'}
    ]

    data = [{"id": row["id"],
             "values": {"PAYLOAD_ID": row["PAYLOAD_ID"],
                        "TRSP_ID": row["TRSP_ID"],
                        "BEAM_RX_CENTER_X_ANT": row["BEAM_RX_CENTER_X_ANT"],
                        "BEAM_RX_CENTER_Y_ANT": row["BEAM_RX_CENTER_Y_ANT"],
                        "BEAM_RX_CENTER_Z_ANT": row["BEAM_RX_CENTER_Z_ANT"],
                        "BEAM_RX_RADIUS": row["BEAM_RX_RADIUS"],
                        "BEAM_TX_CENTER_X_ANT": row["BEAM_TX_CENTER_X_ANT"],
                        "BEAM_TX_CENTER_Y_ANT": row["BEAM_TX_CENTER_Y_ANT"],
                        "BEAM_TX_CENTER_Z_ANT": row["BEAM_TX_CENTER_Z_ANT"],
                        "BEAM_TX_RADIUS": row["BEAM_TX_RADIUS"]
                        }} for row in rows]
    return response.json({"metadata": metadata, 'data': data})


def satellite_table_JSON():
    """
    returns a json for the satellite editablegrid
    :return:
    """
    job_id = request.args(0)
    sat_table = dbLinkBudget.SAT
    rows = dbLinkBudget(sat_table.Job_ID == request.args(0)).select(sat_table.id, sat_table.SAT_ID, sat_table.NADIR_LON,
                                                                    sat_table.NADIR_LAT, sat_table.DISTANCE,
                                                                    sat_table.FOV_RADIUS,
                                                                    sat_table.INCLINATION_ANGLE, sat_table.FLAG_ASC_DESC,
                                                                    sat_table.ROLL, sat_table.PITCH, sat_table.YAW)

    metadata = [
        {"name": "SAT_ID", "label": "SAT ID",
            "datatype": "double", "editable": "true"},
        {"name": "NADIR_LAT", "label": "Nadir Lat",
            "datatype": "double", "editable": "true"},
        {"name": "NADIR_LON", "label": "Nadir Lon",
            "datatype": "double(, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "DISTANCE", "label": "Altitude",
            "datatype": "double(, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "FOV_RADIUS", "label": "Field of View Radius",
            "datatype": "double(deg, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "INCLINATION_ANGLE", "label": "Incl. Angle.",
            "datatype": "double(deg, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "FLAG_ASC_DESC", "label": "ASC/DESC Flag",
            "datatype": "string(, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "ROLL", "label": "Roll",
            "datatype": "double(deg, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "PITCH", "label": "Pitch",
            "datatype": "double(deg, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "YAW", "label": "Yaw",
            "datatype": "double(deg, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "action", "label": "", "datatype": "html", "editable": 'false'}
    ]

    data = [{"id": row["id"],
             "values": {"SAT_ID": row["SAT_ID"],
                        "NADIR_LON": row["NADIR_LON"],
                        "NADIR_LAT": row["NADIR_LAT"],
                        "DISTANCE": row["DISTANCE"],
                        "FOV_RADIUS": row["FOV_RADIUS"],
                        "INCLINATION_ANGLE": row["INCLINATION_ANGLE"],
                        "FLAG_ASC_DESC": row["FLAG_ASC_DESC"],
                        "ROLL": row["ROLL"],
                        "PITCH": row["PITCH"],
                        "YAW": row["YAW"]
                        }} for row in rows]
    return response.json({"metadata": metadata, 'data': data})


def gw_table_JSON():
    """
    returns a json for the gw editablegrid
    :return:
    """
    job_id = request.args(0)
    gw_table = dbLinkBudget.Earth_coord_GW
    rows = dbLinkBudget(gw_table.Job_ID == request.args(0)).select(gw_table.id, gw_table.LAT, gw_table.LON,
                                                                   gw_table.ALT, gw_table.GW_ID)

    metadata = [
        {"name": "GW_ID", "label": "Gateway ID",
            "datatype": "string", "editable": "true"},
        {"name": "LAT", "label": "Latitude",
            "datatype": "double", "editable": "true"},
        {"name": "LON", "label": "Longitude",
            "datatype": "double(, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "ALT", "label": "Altitude",
            "datatype": "double(, 2, dot, comma, 0, n/a)", "editable": "true"},
        {"name": "action", "label": "", "datatype": "html", "editable": 'false'}
    ]

    data = [{"id": row["id"],
             "values": {"GW_ID": row["GW_ID"],
                        "LON": row["LON"],
                        "LAT": row["LAT"],
                        "ALT": row["ALT"]
                        }} for row in rows]
    return response.json({"metadata": metadata, 'data': data})


def json_serial(obj):
    """
    Function needed to serialise the date field for json output

    Args:
        obj:
    """
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
    creates an excel spreadsheet to be downloaded
    #TODO style the spreadsheet and remove unecessary values
    """
    if dbLinkBudget.Calculate(dbLinkBudget.Calculate.Job_ID == request.args(0)):
        sheets = []
        for table in [dbLinkBudget.VSAT, dbLinkBudget.Gateway, dbLinkBudget.SAT, dbLinkBudget.TRSP,
                      dbLinkBudget.Earth_coord_GW, dbLinkBudget.EARTH_coord_VSAT]:
            keys = table.fields
            keys.remove('id')
            keys.remove('Job_ID')
            output = OrderedDict.fromkeys(keys)
            for key in keys:
                output[key] = []
            for row in dbLinkBudget(table.Job_ID == request.args(0)).iterselect(*keys):
                for key in keys:
                    output[key].append(row["_extra"][key])
            sheets.append(output)

        filename = "Link Budget - Output Scenario " + request.args(0) + ".xlsx"
        filepath = os.path.join(request.folder, 'uploads', filename)
        create_saving_worksheet(filepath, sheets[0], "VSAT", sheets[1], "GATEWAY", sheets[2], "SAT", sheets[3], "TRSP",
                                sheets[4], "EARTH_coord_GW", sheets[5], "EARTH_coord_VSAT")
        stream = open(filepath, 'rb')
        dbLinkBudget(dbLinkBudget.Calculate.Job_ID == request.args(0)).update(
            processed_file=dbLinkBudget.Calculate.processed_file.store(stream, filepath))
        redirect(URL('download', args=dbLinkBudget.Calculate(
            dbLinkBudget.Calculate.Job_ID == request.args(0)).processed_file))
    else:
        redirect(URL('download', args=dbLinkBudget.Job(
            dbLinkBudget.Job.id == request.args(0)).file_up))


def SAT_FOV_to_JSON():
    """
    create json with satellite field of view
    :return:
    """
    job_id = request.args(0)
    SAT_dict = datatable_to_dict(dbLinkBudget.SAT, job_id, dbLinkBudget)
    # -----------------  1/ Compute SAT geometric params ------------------
    SAT_dict, nadir_ecef, pos_ecef, normal_vector = compute_sat_params(
        SAT_dict, True)
    write_dict_to_table(dbLinkBudget.SAT, SAT_dict, job_id, dbLinkBudget)
    values = display_sat_field_of_views_for_cesium(nadir_ecef, pos_ecef, normal_vector,
                                                   SAT_dict['FOV_RADIUS'] *
                                                   np.pi / 180,
                                                   SAT_dict['ROLL'] *
                                                   np.pi / 180,
                                                   SAT_dict['PITCH'] *
                                                   np.pi / 180,
                                                   SAT_dict['YAW'] * np.pi / 180)
    coordinates = {}
    for SAT_ID in np.arange(0, np.size(values, 0) / 2):
        coordinates[SAT_ID] = []
        lon = values[2 * SAT_ID, :]
        lat = values[2 * SAT_ID + 1, :]
        for point in range(0, len(values[2 * int(SAT_ID), :])):
            coordinates[SAT_ID].append([lon[point], lat[point]])
        coordinates[SAT_ID].append(coordinates[SAT_ID][0])

    features = [{"type": "Feature",
                 "geometry": {
                     "type": "LineString",
                     "coordinates": coordinates[i]
                 },
                 "properties": {
                     "title": "SAT " + str(i) + " 3dB Field of View"}
                 } for i in coordinates]

    return response.json({"type": "FeatureCollection", 'features': features})


def TRSP_FOV_to_JSON():
    """
    create json with transponder field of views
    :return:
    """
    job_id = request.args(0)
    SAT_dict = datatable_to_dict(dbLinkBudget.SAT, job_id, dbLinkBudget)
    TRSP_dict = datatable_to_dict(dbLinkBudget.TRSP, job_id, dbLinkBudget)
    SAT_dict, nadir_ecef, pos_ecef, normal_vector = compute_sat_params(
        SAT_dict, True)
    coordinates = {}
    for SAT_ID in SAT_dict['SAT_ID']:
        beam_contour_ll = display_2D_sat_and_beams_for_cesium(SAT_ID, SAT_dict['SAT_ID'],
                                                                                   SAT_dict['PAYLOAD_ID'],
                                                                                   nadir_ecef, pos_ecef,
                                                                                   normal_vector,
                                                                                   SAT_dict['ROLL']* np.pi/180,
                                                                                   SAT_dict['PITCH']* np.pi/180,
                                                                                   SAT_dict['YAW']* np.pi/180,
                                                                                   TRSP_dict['PAYLOAD_ID'],
                                                                                   TRSP_dict[
                                                                                       'BEAM_TX_CENTER_X_ANT']* np.pi/180,
                                                                                   TRSP_dict[
                                                                                       'BEAM_TX_CENTER_Y_ANT']* np.pi/180,
                                                                                   TRSP_dict[
                                                                                       'BEAM_TX_CENTER_Z_ANT']* np.pi/180,
                                                                                   TRSP_dict['BEAM_TX_RADIUS']* np.pi/180)
        for TRSP_ID in np.arange(0, np.size(beam_contour_ll, 0) / 2):
            coordinates[SAT_ID, TRSP_ID] = []
            lon = beam_contour_ll[2 * TRSP_ID, :]
            lat = beam_contour_ll[2 * TRSP_ID + 1, :]
            for point in range(0, len(beam_contour_ll[2 * int(TRSP_ID), :])):
                coordinates[SAT_ID, TRSP_ID].append([lon[point], lat[point]])
            coordinates[SAT_ID, TRSP_ID].append(
                coordinates[SAT_ID, TRSP_ID][0])
    features = [{"type": "Feature",
                 "geometry": {
                     "type": "LineString",
                     "coordinates": coordinates[i]
                 },
                 "properties": {
                     "title": "TRSP " + str(i[1]) + " SAT" + str(i[0]) + " \n 3dB Field of View"}
                 } for i in coordinates]
    return response.json({"type": "FeatureCollection", 'features': features})


def run():
    """
    Runs either FWD or RTN mode based on the input form.
    List of functions that call damien's library

    """
    job_id = request.args(0)
    element = dbLinkBudget.Calculate(dbLinkBudget.Calculate.Job_ID == job_id)

    SAT_dict = datatable_to_dict(dbLinkBudget.SAT, job_id, dbLinkBudget)
    TRSP_dict = datatable_to_dict(dbLinkBudget.TRSP, job_id, dbLinkBudget)
    EARTH_COORD_VSAT_dict = datatable_to_dict(
        dbLinkBudget.EARTH_coord_VSAT, job_id, dbLinkBudget)
    EARTH_COORD_GW_dict = datatable_to_dict(
        dbLinkBudget.Earth_coord_GW, job_id, dbLinkBudget)
    GW_dict = datatable_to_dict(dbLinkBudget.Gateway, job_id, dbLinkBudget)
    VSAT_dict = datatable_to_dict(dbLinkBudget.VSAT, job_id, dbLinkBudget)

    if element.simulator_mode == 'FWD':
        # ----------------- 2/ Assign sat to each point of coverage -----------
        EARTH_COORD_VSAT_dict = compute_transponder_assignment(EARTH_COORD_VSAT_dict, SAT_dict, TRSP_dict, 'FWD', 'DN')

        # TODO: here needs to assign a GW to each COV point

        # ----------------- 3/ Compute RX/TX COV geometric params -------------------
        # in that case Rx cov
        EARTH_COORD_VSAT_dict = compute_coverage_points_geo_params(SAT_dict, EARTH_COORD_VSAT_dict, TRSP_dict, 'DN')
        EARTH_COORD_GW_dict = compute_coverage_points_geo_params(SAT_dict, EARTH_COORD_GW_dict, TRSP_dict, 'UP')

        # ----------------- 4/ Compute propag params -------------------
        EARTH_COORD_VSAT_dict = compute_lkb_propag_params(EARTH_COORD_VSAT_dict, SAT_dict, TRSP_dict, VSAT_dict, 'DN', True,
                                                          'FWD')
        EARTH_COORD_GW_dict = compute_lkb_propag_params(EARTH_COORD_GW_dict, SAT_dict, TRSP_dict, GW_dict, 'UP', True,
                                                        'FWD')

        # ----------------- 5/ Compute satellite perfos -------------------
        EARTH_COORD_VSAT_dict = compute_satellite_perfos(EARTH_COORD_VSAT_dict, TRSP_dict, 'DN')
        EARTH_COORD_GW_dict = compute_satellite_perfos(EARTH_COORD_GW_dict, TRSP_dict, 'UP')

    #     # ----------------- 6/ Compute LKB perfos -----------------------
        compute_lkb_CsN0_perfos(EARTH_COORD_GW_dict, EARTH_COORD_VSAT_dict, GW_dict, VSAT_dict, 'FWD', 'compute',
                                'disregard', 'disregard', 'compute', 'disregard')

        compute_lkb_CsN_perfos(EARTH_COORD_GW_dict, EARTH_COORD_VSAT_dict, TRSP_dict, GW_dict, 'FWD')

        compute_spectral_efficiency_and_capacity(EARTH_COORD_VSAT_dict, 'DVB-S2', 'FWD')
    elif element.simulator_mode == 'RTN':

        # ----------------- 2/ Assign sat to each point of coverage -----------
        EARTH_COORD_VSAT_dict = compute_transponder_assignment(EARTH_COORD_VSAT_dict, SAT_dict, TRSP_dict, 'RTN', 'UP')

        # TODO: here needs to assign a GW to each COV point

        # ----------------- 3/ Compute RX/TX COV geometric params -------------------
        # in that case Rx cov
        EARTH_COORD_VSAT_dict = compute_coverage_points_geo_params(SAT_dict, EARTH_COORD_VSAT_dict, TRSP_dict, 'UP')
        EARTH_COORD_GW_dict = compute_coverage_points_geo_params(SAT_dict, EARTH_COORD_GW_dict, TRSP_dict, 'DN')

        # ----------------- 4/ Compute propag params -------------------
        EARTH_COORD_VSAT_dict = compute_lkb_propag_params(EARTH_COORD_VSAT_dict, SAT_dict, TRSP_dict, VSAT_dict, 'UP',
                                                          True, 'RTN')
        EARTH_COORD_GW_dict = compute_lkb_propag_params(EARTH_COORD_GW_dict, SAT_dict, TRSP_dict, GW_dict, 'DN', True,
                                                        'RTN')

        # ----------------- 5/ Compute satellite perfos -------------------
        EARTH_COORD_VSAT_dict = compute_satellite_perfos(EARTH_COORD_VSAT_dict, TRSP_dict, 'UP')
        EARTH_COORD_GW_dict = compute_satellite_perfos(EARTH_COORD_GW_dict, TRSP_dict, 'DN')

        # #----------------- 6/ Compute LKB perfos -----------------------
        compute_lkb_CsN0_perfos(EARTH_COORD_VSAT_dict, EARTH_COORD_GW_dict, VSAT_dict, GW_dict, 'RTN', 'compute',
                                'disregard', 'disregard', 'compute', 'disregard')

        compute_lkb_CsN_perfos(EARTH_COORD_VSAT_dict, EARTH_COORD_GW_dict, TRSP_dict, VSAT_dict, 'RTN')
        #
        compute_spectral_efficiency_and_capacity(EARTH_COORD_VSAT_dict, 'DVB-S2', 'RTN')

    write_dict_to_table(dbLinkBudget.TRSP, TRSP_dict, job_id, dbLinkBudget)
    write_dict_to_table(dbLinkBudget.SAT, SAT_dict, job_id, dbLinkBudget)
    write_dict_to_table(dbLinkBudget.EARTH_coord_VSAT,
                       EARTH_COORD_VSAT_dict, job_id, dbLinkBudget)
    write_dict_to_table(dbLinkBudget.Earth_coord_GW,
                        EARTH_COORD_GW_dict, job_id, dbLinkBudget)

    dbLinkBudget(dbLinkBudget.Calculate.Job_ID ==
                 request.args(0)).update(processed=True)
    redirect(URL('preview', args=request.args(0)))


def cesium():
    """    Cesium viewing page cesium.html    """
    return dict(a=1)


def performance_maxmin():
    """
    Function to extract min and max performance values to scale the plots in cesium.
    args: job_id
    returns: json with max and min for each performance
    """
    earth_vsat = dbLinkBudget.EARTH_coord_VSAT
    rows = dbLinkBudget(earth_vsat.Job_ID == request.args(0)).select(earth_vsat.SAT_EIRP, earth_vsat.ELEVATION,
                                                                     earth_vsat.SAT_GPT, earth_vsat.SAT_GAIN_TX,
                                                                     earth_vsat.SAT_GAIN_RX, earth_vsat.DIST,
                                                                     earth_vsat.FSL_UP, earth_vsat.FSL_DN,
                                                                     earth_vsat.SPEC_EFF, earth_vsat.EFFICIENCY,
                                                                     earth_vsat.CSIM0, earth_vsat.CSIM0,
                                                                     earth_vsat.CSN0_DN, earth_vsat.CSN0_DN,
                                                                     earth_vsat.CSI0_DN, earth_vsat.CSI0_DN,
                                                                     earth_vsat.LON, earth_vsat.LAT)
    EIRP = [[row.SAT_EIRP] for row in rows]
    ELEVATION = [[row.ELEVATION] for row in rows]
    SAT_GPT = [[row.SAT_GPT] for row in rows]
    SAT_GAIN_TX = [[row.SAT_GAIN_TX] for row in rows]
    SAT_GAIN_RX = [[row.SAT_GAIN_RX] for row in rows]
    DIST = [[row.DIST] for row in rows]
    FSL_UP = [[row.FSL_UP] for row in rows]
    FSL_DN = [[row.FSL_DN] for row in rows]
    SPEC_EFF = [[row.SPEC_EFF] for row in rows]
    CSIM0 = [[row.CSIM0] for row in rows]
    CSN0_DN = [[row.CSN0_DN] for row in rows]
    CSI0_DN = [[row.CSI0_DN] for row in rows]
    LAT = [[row.LAT] for row in rows]
    LON = [[row.LON] for row in rows]

    return json.dumps(
        {
    "EIRP": {"max": max(EIRP), "min": min(EIRP)},
    "ELEVATION": {"max": max(ELEVATION), "min": min(ELEVATION)},
    "SAT_GPT": {"max": max(SAT_GPT), "min": min(SAT_GPT)},
    "SAT_GAIN_TX": {"max": max(SAT_GAIN_TX), "min": min(SAT_GAIN_TX)},
    "SAT_GAIN_RX": {"max": max(SAT_GAIN_RX), "min": min(SAT_GAIN_RX)},
    "DIST": {"max": max(DIST), "min": min(DIST)},
    "FSL_UP": {"max": max(FSL_UP), "min": min(FSL_UP)},
    "FSL_DN": {"max": max(FSL_DN), "min": min(FSL_DN)},
    "SPEC_EFF": {"max": max(SPEC_EFF), "min": min(SPEC_EFF)},
    "CSIM0": {"max": max(CSIM0), "min": min(CSIM0)},
    "CSN0_DN": {"max": max(CSN0_DN), "min": min(CSN0_DN)},
    "CSI0_DN": {"max": max(CSI0_DN), "min": min(CSI0_DN)},
    "LAT": {"max": max(LAT), "min": min(LAT)},
    "LON": {"max": max(LON), "min": min(LON)}},
    sort_keys = True, indent = 4, separators = (',', ': '))


def VSATcoverage(lat, lon, npoints, distance):
    """
    Produces 2 arrays

    Usage example:
    VSATcoverage(-90,0,300,.2)
    UNUSED
    """
    sidelength = np.floor(np.sqrt(npoints))
    lonarray_calc = np.arange(
        lon - (distance * sidelength / 2), lon + (distance * sidelength / 2), distance)
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
    latarray_calc = np.arange(
        lat - (distance * sidelength / 2), lat + (distance * sidelength / 2), distance)
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


def get_performance_json():
    """
    Function to get the coordinates into a GeoJSON format
    This adds the lat and longitude for the User Terminals
    Called in cesium.html

    Returns:
        object: GeoJSON
    """
    earth_vsat = dbLinkBudget.EARTH_coord_VSAT
    # I think putting the fields in the brackets will speed up the query
    earth_vsat_rows = dbLinkBudget(earth_vsat.Job_ID == request.args(
        0)).select()  # TODO : test if iterselect is better than regular select, time and memory
    # resources.
    features = []
    i=0
    for row in earth_vsat_rows:
        features.append({"type": "Feature",
                         "geometry": {
                             "type": "Point",
                             "coordinates": [row[earth_vsat.LON], row[earth_vsat.LAT]]
                         },
                         "properties": OrderedDict({
                             "Job ID": row[earth_vsat.Job_ID],
                             "title": [str(row[earth_vsat.VSAT_ID])],
                             "Lon, Lat": str(row[earth_vsat.LON]) + ", " + str(row[earth_vsat.LAT]),
                         })
                         })  # TODO : Extend to include more information from db
        features[i]["properties"].update({"SAT_ID, TRSP_ID, PAYLOAD_ID": str(row[earth_vsat.SAT_ID]) + ", " + str(row[earth_vsat.TRSP_ID]) + ", " + str(row[earth_vsat.PAYLOAD_ID])})
        if row[earth_vsat.ELEVATION]:
            features[i]["properties"].update({"ELEVATION": round(row[earth_vsat.ELEVATION], 2)})
        if row[earth_vsat.SAT_EIRP]:
            features[i]["properties"].update({"EIRP": round(row[earth_vsat.SAT_EIRP], 2)})
        if row[earth_vsat.SAT_GPT]:
            features[i]["properties"].update({ "SAT_GPT": round(row[earth_vsat.SAT_GPT], 2)})
        if row[earth_vsat.SAT_GAIN_TX]:
            features[i]["properties"].update({ "SAT_GAIN_TX": round(row[earth_vsat.SAT_GAIN_TX], 2)})
        if row[earth_vsat.SAT_GAIN_RX]:
            features[i]["properties"].update({ "SAT_GAIN_RX": round(row[earth_vsat.SAT_GAIN_RX], 2)})
        if row[earth_vsat.DIST]:
            features[i]["properties"].update({ "DIST": round(row[earth_vsat.DIST], 2)})
        if row[earth_vsat.FSL_UP]:
            features[i]["properties"].update({ "FSL_UP": round(row[earth_vsat.FSL_UP], 2)})
        if row[earth_vsat.FSL_DN]:
            features[i]["properties"].update({ "FSL_DN": round(row[earth_vsat.FSL_DN], 2)})
        if row[earth_vsat.EFFICIENCY]:
            features[i]["properties"].update({ "EFFICIENCY": round(row[earth_vsat.EFFICIENCY], 2)})
        if row[earth_vsat.CSIM0]:
            features[i]["properties"].update({ "CSIM0": round(row[earth_vsat.CSIM0], 2)})
        if row[earth_vsat.CSN0_DN]:
            features[i]["properties"].update({ "CSN0_DN": round(row[earth_vsat.CSN0_DN], 2)})
        if row[earth_vsat.CSI0_DN]:
            features[i]["properties"].update({ "CSI0_DN": round(row[earth_vsat.CSI0_DN], 2)})
        i+=1
    return response.json({"type": "FeatureCollection", 'features': features})


def get_geojson_gw():
    """
    Function to get the coordinates into a GeoJSON format
    This adds the lat and longitudes for the gateways
    Called in cesium.html

    Returns:
        object: GeoJSON
    """
    earth_gateway = dbLinkBudget.Earth_coord_GW
    earth_gateway_rows = dbLinkBudget(earth_gateway.Job_ID == request.args(0)).iterselect(earth_gateway.LON,
                                                                                          earth_gateway.LAT,
                                                                                          earth_gateway.Job_ID,
                                                                                          earth_gateway.GW_ID)

    features = [{"type": "Feature",
                 "geometry": {
                     "type": "Point",
                     "coordinates": [row[earth_gateway.LON], row[earth_gateway.LAT]]
                 },
                 "properties": {
                     "title": "Gateway",
                     "Job ID": row[earth_gateway.Job_ID],
                     "Gateway ID": row[earth_gateway.GW_ID],
                     "EIRP Max": dbLinkBudget.Gateway(
                         dbLinkBudget.Gateway.GW_ID == row[earth_gateway.GW_ID]).EIRP_MAX,
                     "Bandwidth": dbLinkBudget.Gateway(
                         dbLinkBudget.Gateway.GW_ID == row[earth_gateway.GW_ID]).BANDWIDTH,
                     "Diameter": dbLinkBudget.Gateway(
                         dbLinkBudget.Gateway.GW_ID == row[earth_gateway.GW_ID]).DIAMETER,
                     "Lat": row[earth_gateway.LAT],
                     "Lon, Lat": str(row[earth_gateway.LON]) + ", " + str(row[earth_gateway.LAT])
                 }
                 } for row in earth_gateway_rows]
    return response.json({"type": "FeatureCollection", 'features': features})


def get_geojson_sat():
    """
    Function to get the coordinates into a GeoJSON format
    This adds the lat and longitudes for the SAT
    Called in cesium.html

    Returns:
        object: GeoJSON
    """
    satellite_rows = dbLinkBudget(
        dbLinkBudget.SAT.Job_ID == request.args(0)).iterselect()
    satellite = dbLinkBudget.SAT
    features = [{"type": "Feature",
                 "geometry": {
                     "type": "Point",
                     "coordinates": [row[satellite.NADIR_LON],
                                     row[satellite.NADIR_LAT],
                                     row[satellite.DISTANCE] *
                                     1000  # convert to metres
                                     ]
                 },
                 "properties": {
                     "title": "SAT" + " " + str(int(row[satellite.SAT_ID])),
                     "Height (km)": row[satellite.DISTANCE],
                     "Field of View (degrees)": row[satellite.FOV_RADIUS],
                     "Payload ID": row[satellite.PAYLOAD_ID],
                     "Lon, Lat": str(row[satellite.NADIR_LON]) + "," + str(row[satellite.NADIR_LAT]),
                 }
                 } for row in satellite_rows]
    return response.json({"type": "FeatureCollection", 'features': features})





def json_subsatellite():
    """
    line from satellite to ground
    """
    satellite_rows = dbLinkBudget(
        dbLinkBudget.SAT.Job_ID == request.args(0)).iterselect()
    satellite = dbLinkBudget.SAT

    features = [{"type": "Feature",
                 "geometry": {
                     "type": "LineString",
                     "coordinates":[
                                    [row[satellite.NADIR_LON],
                                     row[satellite.NADIR_LAT],
                                    0
                                     ],
                                     [row[satellite.NADIR_LON],
                                     row[satellite.NADIR_LAT],
                                     row[satellite.DISTANCE] *  1000  # convert to metres
                                    ]]
                                },
                 "properties": {
                     "title": "SAT " + str(row[satellite.SAT_ID])}
                 } for row in satellite_rows]

    return response.json({"type": "FeatureCollection", 'features': features})


def get_geojson_FOV():
    """
    Function to get the coordinates into a GeoJSON format
    This adds the lat and longitudes for the SAT
    Called in cesium.html

    Returns:
        object: GeoJSON
    """
    satellite = dbLinkBudget.SAT
    satellite_rows = dbLinkBudget(
        satellite.Job_ID == request.args(0)).iterselect()

    features = [{"type": "Feature",
                 "geometry": {
                     "type": "Point",
                     "coordinates": [row[satellite.NADIR_LON],
                                     row[satellite.NADIR_LAT],
                                     row[satellite.DISTANCE] * 1000 / 2
                                     # centre of the cone is half way from
                                     # ground to satellites
                                     ]
                 },
                 "properties": {
                     "title": "SAT" + " " + str(row[satellite.SAT_ID]) + " Cone",
                     "Height": row[satellite.DISTANCE],
                     "BottomRadius": round(row[satellite.DISTANCE] * 1000 * np.tan(
                         (np.pi / 180) * row[satellite.FOV_RADIUS])),
                     # radius of bottom of cone is D*tan(theta) where theta is
                     # the half angle at the top of the cone
                     "Payload ID": row[satellite.PAYLOAD_ID],
                 }
                 } for row in satellite_rows]
    return response.json({"type": "FeatureCollection", 'features': features})


@request.restful()
def api():
    response.view = 'generic.' + request.extension

    def GET(*args, **vars):
        patterns = 'auto'
        parser = dbLinkBudget.parse_as_rest(patterns, args, vars)
        if parser.status == 200:
            return dict(content=parser.response)
        else:
            raise HTTP(parser.status, parser.error)

    return dict(GET=GET)
