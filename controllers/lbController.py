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
import time

from collections import defaultdict

from excelHandling import *
from gluon import *
from lib_lkb.compute_high_level_func import *
from lib_lkb.display_func import *

import platform

if platform.system() is 'Windows':
    from lib_lkb.propa_func_windows import *
elif platform.system() is 'Linux':
    from lib_lkb.propa_func_linux import *

response.title = 'Orbitool'


def index():
    """ Home Page """
    return dict(message=T(''))


def about():
    """ About page """
    return dict(message=T('About'))


def input():
    """ Input form """  # TODO: Think about adding drag and drop plugin
    # TODO : separate the form
    session.job = ""
    record = dbLinkBudget.Job(request.args(0))
    dbLinkBudget.Job.Date.readable = False
    form = SQLFORM(dbLinkBudget.Job, record, deletable=True,
                   upload=URL('download'), formstyle='table3cols')
    if form.process().accepted:
        session.flash = "%s - %s has been accepted" % (form.vars.id, form.vars.job_name)
        session.job = form.vars.job_name
        add_excel_2_db()
    elif form.errors:
        session.flash = "%s - %s has FAILED" % (form.vars.id, form.vars.job_name)
    return dict(form=form)


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
    job_id = request.args(0)
    if dbLinkBudget.Job(job_id):
        job = json.dumps(dbLinkBudget(dbLinkBudget.Job).select().as_list(),
                         default=json_serial)  # default json.dumps specificed

        gw = dbLinkBudget(dbLinkBudget.Gateway.Job_ID == job_id).select().as_list()
        vsat = dbLinkBudget(dbLinkBudget.VSAT.Job_ID == job_id).select().as_list()
        sat = dbLinkBudget(dbLinkBudget.SAT.Job_ID == job_id).select().as_list()
        trsp = dbLinkBudget(dbLinkBudget.TRSP.Job_ID == job_id).select().as_list()

        record = dbLinkBudget.Job(request.args(0))
        dbLinkBudget.Job.Date.readable = False
        dbLinkBudget.Job.file_up.readable = False
        dbLinkBudget.Job.file_up.writable = False
        form = SQLFORM(dbLinkBudget.Job, record, deletable=True, formstyle='table3cols', submit_button='Update')

        form.add_button('Next', URL('launch', args=request.args(0)))
        if form.process().accepted:
            session.flash = "%s - %s has been updated" % (form.vars.id, form.vars.job_name)
            if form.deleted:
                session.flash = "%s) %s has been deleted" % (form.vars.id, form.vars.job_name)
                redirect(URL('select'))
            elif form.errors:
                session.job = form.vars.job_name
                session.flash = "Errors in form"
        return dict(job=XML(job), vsat=XML(json.dumps(vsat)), gw=XML(json.dumps(gw)), sat=XML(json.dumps(sat)),
                    trsp=XML(json.dumps(trsp)), form=form)
    else:
        redirect(URL('input'))


def launch():
    """
    Run page


    """
    session.job = ""
    job_id = request.args(0)
    dbLinkBudget.Calculate.processed.readable = False  # enable these when in use. Having it off is good for debugging
    dbLinkBudget.Calculate.processed.writable = False
    dbLinkBudget.Calculate.Job_ID.writable = False
    if dbLinkBudget.Job(job_id):
        record = dbLinkBudget.Calculate(dbLinkBudget.Calculate.Job_ID == job_id)
        form = SQLFORM(dbLinkBudget.Calculate, record, showid=False, formstyle='table3cols', submit_button='Save')
        form.add_button('Select Page', URL('select'))
        if form.process().accepted:
            session.flash = "%s -  has been updated" % (form.vars.id)
            if form.deleted:
                session.flash = "%s)  has been deleted" % (form.vars.id)
                redirect(URL('select'))
            elif form.errors:
                session.job = form.vars.job_name
        return dict(form=form)
    else:
        redirect(URL('input'))


def add_excel_2_db():
    """
    Function used to insert excel dictionary into database

    """
    fileName = dbLinkBudget.Job(dbLinkBudget.Job.job_name == session.job).file_up  # Find uploaded file
    job_id = dbLinkBudget.Job(dbLinkBudget.Job.job_name == session.job).id
    excel_info = load_objects_from_xl(os.path.join(request.folder, 'uploads', fileName))
    write_dict_to_table(dbLinkBudget.SAT, excel_info[0], job_id)
    write_dict_to_table(dbLinkBudget.TRSP, excel_info[1], job_id)
    write_dict_to_table(dbLinkBudget.VSAT, excel_info[2], job_id)
    write_dict_to_table(dbLinkBudget.Earth_coord_GW, excel_info[3], job_id)
    write_dict_to_table(dbLinkBudget.Gateway, excel_info[4], job_id)
    write_dict_to_table(dbLinkBudget.EARTH_coord_VSAT, excel_info[5], job_id)

    redirect(URL('preview', args=job_id))


def preview():
    # SQL GRID
    # process submitted form
    if len(request.post_vars) > 0:
        for key, value in request.post_vars.iteritems():
            (field_name, sep, row_id) = key.partition('_row_')  # name looks like home_state_row_99
            if row_id:
                dbLinkBudget(dbLinkBudget.SAT.id == row_id).update(**{field_name: value})

                # the name attribute is the method we know which row is involved1.0

    dbLinkBudget.SAT.SAT_ID.represent = lambda value, row: string_widget(dbLinkBudget.SAT.SAT_ID, value,
                                                                         **{'_name': 'SAT_ID_row_%s' % row.id})
    dbLinkBudget.SAT.NADIR_LON.represent = lambda value, row: string_widget(dbLinkBudget.SAT.NADIR_LON, value,
                                                                            **{'_name': 'NADIR_LON_row_%s' % row.id})
    dbLinkBudget.SAT.NADIR_LAT.represent = lambda value, row: string_widget(dbLinkBudget.SAT.NADIR_LAT, value,
                                                                            **{'_name': 'NADIR_LAT_row_%s' % row.id})
    dbLinkBudget.SAT.DISTANCE.represent = lambda value, row: string_widget(dbLinkBudget.SAT.DISTANCE, value,
                                                                           **{'_name': 'DISTANCE_row_%s' % row.id})

    dbLinkBudget.SAT.FOV_RADIUS.represent = lambda value, row: string_widget(dbLinkBudget.SAT.FOV_RADIUS, value,
                                                                             **{'_name': 'FOV_RADIUS_row_%s' % row.id})

    dbLinkBudget.SAT.id.readable = False
    dbLinkBudget.SAT.Job_ID.readable = False
    dbLinkBudget.SAT.INCLINATION_ANGLE.readable = False
    dbLinkBudget.SAT.FLAG_ASC_DESC.readable = False
    dbLinkBudget.SAT.INTERF_FLAG.readable = False
    dbLinkBudget.SAT.ROLL.readable = False
    dbLinkBudget.SAT.PITCH.readable = False
    dbLinkBudget.SAT.YAW.readable = False
    dbLinkBudget.SAT.PAYLOAD_ID.readable = False
    dbLinkBudget.SAT.NADIR_X_ECEF.readable = False
    dbLinkBudget.SAT.NADIR_Y_ECEF.readable = False
    dbLinkBudget.SAT.NADIR_Z_ECEF.readable = False
    dbLinkBudget.SAT.SAT_POS_X_ECEF.readable = False
    dbLinkBudget.SAT.SAT_POS_Y_ECEF.readable = False
    dbLinkBudget.SAT.SAT_POS_Z_ECEF.readable = False
    dbLinkBudget.SAT.NORMAL_VECT_X.readable = False
    dbLinkBudget.SAT.NORMAL_VECT_Y.readable = False
    dbLinkBudget.SAT.NORMAL_VECT_Z.readable = False

    grid = SQLFORM.grid(dbLinkBudget.SAT.Job_ID == request.args(0), details=False, deletable=True, user_signature=False,
                        csv=False, paginate=5,
                        editable=True, args=request.args[:1],
                        selectable=lambda ids: redirect(URL('lbController', 'preview', args=request.args(0))),
                        )  # preserving _get_vars means user goes back to same grid page, same sort options etc

    grid.element(_type='submit', _value='%s' % T('Submitttt'))
    grid.elements(_type='checkbox', _name='records', replace=None)  # remove selectable's checkboxes

    # SQL FORM


    session.job = ""
    job_id = request.args(0)
    dbLinkBudget.Calculate.processed.readable = False  # enable these when in use. Having it off is good for debugging
    dbLinkBudget.Calculate.processed.writable = False
    dbLinkBudget.Calculate.Job_ID.writable = False
    record = dbLinkBudget.Calculate(dbLinkBudget.Calculate.Job_ID == job_id)
    form = SQLFORM(dbLinkBudget.Calculate, record, showid=False, formstyle='table3cols', submit_button='Save')
    if form.process().accepted:
        session.flash = "%s -  has been updated" % (form.vars.id)
        if form.deleted:
            session.flash = "%s)  has been deleted" % (form.vars.id)
            redirect(URL('select'))
        elif form.errors:
            session.job = form.vars.job_name
    return dict(grid=grid, form=form)

def write_dict_to_table(db, ordDict, job_id):
    # type: (object, object, object) -> object
    """
    Used to read in dictionaries which contain
    np arrays created when reading excel file

    Args:
        db: database
        ordDict: OrderedDict
        job_id:

    """
    row = ordDict.fromkeys(ordDict)
    for v in range(ordDict.values()[0].size):
        for k in range(len(ordDict.keys())):
            row[ordDict.keys()[k]] = ordDict.values()[k][v]
        # insert to database, but check if the fields already exist
        job_id_check = db.Job_ID == job_id
        if db is dbLinkBudget.Gateway:
            db.update_or_insert((db.GW_ID == row['GW_ID']) & (job_id_check), Job_ID=job_id,
                                **row)
        elif db is dbLinkBudget.SAT:
            dbLinkBudget.SAT.update_or_insert((db.SAT_ID == row['SAT_ID']) & (job_id_check), Job_ID=job_id, **row)
        elif db is dbLinkBudget.TRSP:
            db.update_or_insert((db.TRSP_ID == row['TRSP_ID']) & (job_id_check), Job_ID=job_id, **row)
        elif db is dbLinkBudget.VSAT:
            db.update_or_insert((db.VSAT_ID == row['VSAT_ID']) & (job_id_check), Job_ID=job_id, **row)
        elif db is dbLinkBudget.Earth_coord_GW:
            db.update_or_insert(
                (job_id_check) & (db.LON == row['LON']) & (db.LAT == row['LAT']) & (db.GW_ID == row['GW_ID']) & (
                    db.TRSP_ID == row['TRSP_ID']), Job_ID=job_id, **row)
        elif db is dbLinkBudget.EARTH_coord_VSAT:
            db.update_or_insert(
                (job_id_check) & (db.LON == row['LON']) & (db.LAT == row['LAT']) & (
                    db.VSAT_ID == row['VSAT_ID']), Job_ID=job_id, **row)
        else:
            db.update_or_insert(Job_ID=job_id, **row)

def testtest():
    return datatable_to_dict(dbLinkBudget.SAT, 1)



def datatable_to_dict(table, job_id):
    """
    Reads dicts of numpy arrays from database
    """
    keys = list(table.fields)
    keys.remove("Job_ID")
    keys.remove("id")
    mydict = defaultdict(list)
    row_list=dbLinkBudget(table.Job_ID == job_id).iterselect(*keys).as_list()
    for row in range(0,len(row_list)):
        for key, value in row_list[row]['_extra'].items():
            mydict[key] = np.append(mydict[key],value)
    return mydict


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
    Creates downloadable file.
    This is called in update.html under options

    TODO: consider using lists instead of dictionaries so that the download excel is ordered.
    TODO: at RX fields
    """
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
    dbLinkBudget(dbLinkBudget.Calculate.id == request.args(0)).update(
        processed_file=dbLinkBudget.Calculate.processed_file.store(stream, filepath))
    os.remove(filepath)
    redirect(URL('download', args=dbLinkBudget.Calculate(dbLinkBudget.Calculate.id == request.args(0)).processed_file))


def benchmark():
    time1 = time.time()
    job_id = 1
    SAT_dict = datatable_to_dict(dbLinkBudget.SAT, job_id)
    TRSP_dict = datatable_to_dict(dbLinkBudget.TRSP, job_id)
    EARTH_COORD_VSAT_dict = datatable_to_dict(dbLinkBudget.EARTH_coord_VSAT, job_id)
    EARTH_COORD_GW_dict = datatable_to_dict(dbLinkBudget.Earth_coord_GW, job_id)
    GW_dict = datatable_to_dict(dbLinkBudget.Gateway, job_id)
    VSAT_dict = datatable_to_dict(dbLinkBudget.VSAT, job_id)
    return time.time() - time1

def benchmarkexcel():
    time2 = time.time()
    fileName = dbLinkBudget.Job(dbLinkBudget.Job.id == 1).file_up  # Find uploaded file
    excel_info = load_objects_from_xl(os.path.join(request.folder, 'uploads', fileName))
    SAT_dict = excel_info[0]
    TRSP_dict = excel_info[1]
    logger.error(time.time() - time2)
    return {1:SAT_dict, 2:TRSP_dict, 3: excel_info[2], 4:excel_info[3], 5:excel_info[4], 6:excel_info[5]}

def calculate_geometrics():
    job_id = request.args(0)
    element = dbLinkBudget.Calculate(dbLinkBudget.Calculate.Job_ID == job_id)

    SAT_dict = datatable_to_dict(dbLinkBudget.SAT, job_id)
    TRSP_dict = datatable_to_dict(dbLinkBudget.TRSP, job_id)
    # -----------------  1/ Compute SAT geometric params ------------------
    SAT_dict, nadir_ecef, pos_ecef, normal_vector = compute_sat_params(SAT_dict, True)

    values = display_sat_field_of_views_for_cesium(nadir_ecef, pos_ecef, normal_vector, \
                                                   SAT_dict['FOV_RADIUS'] * np.pi / 180, \
                                                   SAT_dict['ROLL'] * np.pi / 180, \
                                                   SAT_dict['PITCH'] * np.pi / 180, \
                                                   SAT_dict['YAW'] * np.pi / 180)
    lat = np.array([])
    lon = np.array([])
    count = np.array([])
    for i in np.arange(0, np.size(values, 0) / 2):
        lon = np.append(lon, values[2 * i, :])
        lat = np.append(lat, values[2 * i + 1, :])
        count = np.append(count, np.full(len(values[2 * i, :]), i + 1))
        sat_fov_dict = {'SAT_ID': count, 'LON': lon, 'LAT': lat}
    dbLinkBudget(dbLinkBudget.SAT_FOV.Job_ID == job_id).delete()
    write_dict_to_table(dbLinkBudget.SAT_FOV, sat_fov_dict, job_id)

    for SAT_ID in SAT_dict['SAT_ID']:
        dbLinkBudget(dbLinkBudget.TRSP_FOV.Job_ID == job_id).delete()
        beam_centers_lonlat, beam_contour_ll = display_2D_sat_and_beams_for_cesium(SAT_ID, SAT_dict['SAT_ID'],
                                                                                   SAT_dict['PAYLOAD_ID'],
                                                                                   nadir_ecef, pos_ecef,
                                                                                   normal_vector, \
                                                                                   TRSP_dict['PAYLOAD_ID'],
                                                                                   TRSP_dict[
                                                                                       'BEAM_TX_CENTER_AZ_ANT'],
                                                                                   TRSP_dict[
                                                                                       'BEAM_TX_CENTER_EL_ANT'],
                                                                                   TRSP_dict['BEAM_TX_RADIUS'])
        lat = np.array([])
        lon = np.array([])
        count = np.array([])
        SAT_IDs = np.array([])
        for i in np.arange(0, np.size(beam_contour_ll, 0) / 2):
            lon = np.append(lon, beam_contour_ll[2 * i, :])
            lat = np.append(lat, beam_contour_ll[2 * i + 1, :])
            count = np.append(count, np.full(len(beam_contour_ll[2 * i, :]), i + 1))
            SAT_IDs = np.append(SAT_IDs, np.full(len(beam_contour_ll[2 * i, :]), SAT_ID))
            trsp_fov_dict = {'SAT_ID': SAT_IDs, 'TRSP_ID': count, 'LON': lon, 'LAT': lat}
        write_dict_to_table(dbLinkBudget.TRSP_FOV, trsp_fov_dict, job_id)
    write_dict_to_table(dbLinkBudget.SAT, SAT_dict, job_id)
    redirect(URL('preview', args=request.args(0)))

def run():
    """
    This runs the processing of the excel file.
    Currently asks which propagation library is being used.
    Adds EIRP values (in fact it outputs temperature at the moment)
    Updates 'processed' checkbox.

    Returns:
        Refreshes the update page

    """
    job_id = request.args(0)
    element = dbLinkBudget.Calculate(dbLinkBudget.Calculate.Job_ID == job_id)

    SAT_dict = datatable_to_dict(dbLinkBudget.SAT, job_id)
    TRSP_dict = datatable_to_dict(dbLinkBudget.TRSP, job_id)
    EARTH_COORD_VSAT_dict = datatable_to_dict(dbLinkBudget.EARTH_coord_VSAT, job_id)
    EARTH_COORD_GW_dict = datatable_to_dict(dbLinkBudget.Earth_coord_GW, job_id)
    GW_dict = datatable_to_dict(dbLinkBudget.Gateway, job_id)
    VSAT_dict = datatable_to_dict(dbLinkBudget.VSAT, job_id)

    if element.sat_geo_params:
        # -----------------  1/ Compute SAT geometric params ------------------
        SAT_dict, nadir_ecef, pos_ecef, normal_vector = compute_sat_params(SAT_dict, True)

    # ----------------- 2/ Assign sat to each point of coverage -----------
    if element.points2trsp:
        EARTH_COORD_VSAT_dict = compute_transponder_assignment(EARTH_COORD_VSAT_dict,
                                                               SAT_dict, TRSP_dict, element.simulator_mode,
                                                               'DN' if element.simulator_mode == 'FWD' else 'UP')

    if element.gw2trsp:
        EARTH_COORD_GW_dict = compute_transponder_assignment(EARTH_COORD_GW_dict, SAT_dict, TRSP_dict, element
                                                             .simulator_mode,
                                                             'UP' if element.simulator_mode == 'FWD' else 'DN')

    # ----------------- 3/ Compute RX/TX COV geometric params -------------------
    if element.comp_point_cover:
        EARTH_COORD_VSAT_dict = compute_coverage_points_geo_params(SAT_dict, EARTH_COORD_VSAT_dict)

    if element.comp_gw_cover:
        EARTH_COORD_GW_dict = compute_coverage_points_geo_params(SAT_dict, EARTH_COORD_GW_dict)

    # ----------------- 4/ Compute propag params -------------------
    if element.propa_feeder_link:
        EARTH_COORD_GW_dict = compute_lkb_propag_params(EARTH_COORD_GW_dict, SAT_dict, TRSP_dict, GW_dict,
                                                        'UP' if element.simulator_mode == 'FWD' else 'DN', True,
                                                        element.simulator_mode)

    if element.propa_user_link:
        EARTH_COORD_VSAT_dict = compute_lkb_propag_params(EARTH_COORD_VSAT_dict, SAT_dict, TRSP_dict, VSAT_dict,
                                                          'DN' if element.simulator_mode == 'FWD' else 'UP', True,
                                                          element.simulator_mode)

    # ----------------- 5/ Compute satellite perfos -------------------
    if element.sat_up_perf:
        EARTH_COORD_VSAT_dict = compute_satellite_perfos(EARTH_COORD_VSAT_dict, TRSP_dict, 'UP')
    if element.sat_dwn_perf:
        EARTH_COORD_VSAT_dict = compute_satellite_perfos(EARTH_COORD_VSAT_dict, TRSP_dict, 'DN')
    # else:
    #    session.flash = "You need to choose a calculation to launch"
    #    redirect(URL('launch', args=request.args(0)))
    write_dict_to_table(dbLinkBudget.TRSP, TRSP_dict, job_id)  # at the moment these write to new lines
    write_dict_to_table(dbLinkBudget.SAT, SAT_dict, job_id)
    write_dict_to_table(dbLinkBudget.EARTH_coord_VSAT, EARTH_COORD_VSAT_dict, job_id)
    write_dict_to_table(dbLinkBudget.Earth_coord_GW, EARTH_COORD_GW_dict, job_id)

    dbLinkBudget(dbLinkBudget.Calculate.id == request.args(0)).update(processed=True)
    redirect(URL('preview', args=request.args(0)))


def cesium():
    """    Cesium viewing page cesium.html    """
    return dict(a=1)


def copy():  # TODO: Add all of the new fields to this list
    """
    Function for a copy button on update.html.
    It copies the currently viewed data entry to a new row and renames it _copy

    """
    a = dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0))
    filename, stream = dbLinkBudget.Job.file_up.retrieve(a.file_up)
    dbLinkBudget.Job.insert(job_name='%s_copy' % (a.job_name),
                            Date=request.now,
                            file_up=dbLinkBudget.Job.file_up.store(stream, filename),  # this needs to be renamed
                            simulator_mode=a.simulator_mode,
                            sat_geo_params=a.sat_geo_params,
                            points2trsp=a.points2trsp,
                            gw2trsp=a.gw2trsp,
                            comp_point_cover=a.comp_point_cover,
                            comp_gw_cover=a.comp_gw_cover,
                            propa_feeder_link=a.propa_feeder_link,
                            propa_user_link=a.propa_user_link,
                            sat_up_perf=a.sat_up_perf,
                            sat_dwn_perf=a.sat_dwn_perf,
                            comp_link_budget=a.comp_link_budget,
                            description=a.description,
                            processed=a.processed)
    session.flash = "%s has been copied" % (request.args(0))
    redirect(URL('select'))


def performance_maxmin():
    """
    Function to extract min and max performance values to scale the plots in cesium.
    args: job_id
    returns: json with max and min for each performance
    """
    earth_vsat = dbLinkBudget.EARTH_coord_VSAT
    rows = dbLinkBudget(earth_vsat.Job_ID == request.args(0)).select(earth_vsat.SAT_EIRP, earth_vsat.ELEVATION,
                                                                     earth_vsat.SAT_GPT)
    EIRP = [[row.SAT_EIRP] for row in rows]
    ELEVATION = [[row.ELEVATION] for row in rows]
    SAT_GPT = [[row.SAT_GPT] for row in rows]
    return json.dumps(
        {"EIRP": {"max": max(EIRP), "min": min(EIRP)}, "ELEVATION": {"max": max(ELEVATION), "min": min(ELEVATION)},
         "SAT_GPT": {"max": max(SAT_GPT), "min": min(SAT_GPT)}},
        sort_keys=True, indent=4, separators=(',', ': '))


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

def test1():
    fileName = dbLinkBudget.Job(dbLinkBudget.Job.id == 14).file_up
    excel_info = load_objects_from_xl(os.path.join(request.folder, 'uploads', fileName))
    return excel_info[1]
def test2():
    return datatable_to_dict(dbLinkBudget.SAT, 1)

def testthis():
    return VSATcoverage(-90., 0., 300.,
                        0.2)  # you need to convert the output from a np array to something else to show it in a
    # browser. Or do eg lonarray[3]

def get_geojson():
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
        0)).select(earth_vsat.LON, earth_vsat.LAT, earth_vsat.VSAT_ID, earth_vsat.Job_ID, earth_vsat.SAT_EIRP,
                   earth_vsat.ELEVATION,
                   earth_vsat.SAT_GPT)  # TODO : test if iterselect is better than regular select, time and memory
    # resources.
    features = []
    for row in earth_vsat_rows:
        if row[earth_vsat.SAT_EIRP] and not row[earth_vsat.SAT_GPT]:
            features.append({"type": "Feature",
                         "geometry": {
                             "type": "Point",
                             "coordinates": [row[earth_vsat.LON], row[earth_vsat.LAT]]
                         },
                         "properties": {
                             "title": [str(row[earth_vsat.VSAT_ID])],
                             "Job ID": row[earth_vsat.Job_ID],
                             "EIRP": round(row[earth_vsat.SAT_EIRP],2),
                             "ELEVATION": round(row[earth_vsat.ELEVATION],2),
                             "Lon, Lat": str(row[earth_vsat.LON]) + ", " + str(row[earth_vsat.LAT]),
                         }
                         })  # TODO : Extend to include more information form
            # database #hacky way to ignore NONEs
        elif row[earth_vsat.SAT_GPT] and not row[earth_vsat.SAT_EIRP]:
            features.append({"type": "Feature",
                         "geometry": {
                             "type": "Point",
                             "coordinates": [row[earth_vsat.LON], row[earth_vsat.LAT]]
                         },
                         "properties": {
                             "title": [str(row[earth_vsat.VSAT_ID])],
                             "Job ID": row[earth_vsat.Job_ID],
                             "ELEVATION": round(row[earth_vsat.ELEVATION],2),
                             "SAT_GPT": round(row[earth_vsat.SAT_GPT],2),
                             "Lon, Lat": str(row[earth_vsat.LON]) + ", " + str(row[earth_vsat.LAT]),
                         }
                         })  # TODO : Extend to include more information form
            # database #hacky way to ignore NONEs
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
    satellite_rows = dbLinkBudget(dbLinkBudget.SAT.Job_ID == request.args(0)).iterselect()
    satellite = dbLinkBudget.SAT
    features = [{"type": "Feature",
                 "geometry": {
                     "type": "Point",
                     "coordinates": [row[satellite.NADIR_LON],
                                     row[satellite.NADIR_LAT],
                                     row[satellite.DISTANCE] * 1000  # convert to metres
                                     ]
                 },
                 "properties": {
                     "title": "SAT" + " " + str(row[satellite.SAT_ID]),
                     "Height (km)": row[satellite.DISTANCE],
                     "Field of View (degrees)": row[satellite.FOV_RADIUS],
                     "Payload ID": row[satellite.PAYLOAD_ID],
                     "Lon, Lat": str(row[satellite.NADIR_LON]) + "," + str(row[satellite.NADIR_LAT]),
                 }
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
    satellite_rows = dbLinkBudget(satellite.Job_ID == request.args(0)).iterselect()

    features = [{"type": "Feature",
                 "geometry": {
                     "type": "Point",
                     "coordinates": [row[satellite.NADIR_LON],
                                     row[satellite.NADIR_LAT],
                                     row[satellite.DISTANCE] * 1000 / 2
                                     # centre of the cone is half way from ground to satellites
                                     ]
                 },
                 "properties": {
                     "title": "SAT" + " " + str(row[satellite.SAT_ID]) + " Cone",
                     "Height": row[satellite.DISTANCE],
                     "BottomRadius": round(row[satellite.DISTANCE] * 1000 * np.tan(
                         (np.pi / 180) * row[satellite.FOV_RADIUS])),
                     # radius of bottom of cone is D*tan(theta) where theta is the half angle at the top of the cone
                     "Payload ID": row[satellite.PAYLOAD_ID],
                 }
                 } for row in satellite_rows]
    return response.json({"type": "FeatureCollection", 'features': features})


def get_geojson_FOV_CIRCLE():
    """
    Function to get the coordinates into a GeoJSON format
    This adds the lat and longitudes for the SAT
    Called in cesium.html

    Returns:
        object: GeoJSON
    """
    satellite_fov = dbLinkBudget.SAT_FOV
    rows = dbLinkBudget((satellite_fov.Job_ID == request.args(0))).iterselect()
    coordinates = {}

    for row in rows:
        if row[satellite_fov.SAT_ID] not in coordinates:
            coordinates[row[satellite_fov.SAT_ID]] = []
        coordinates[row[satellite_fov.SAT_ID]].append(
            [row[satellite_fov.LON], row[satellite_fov.LAT]])

    features = [{"type": "Feature",
                 "geometry": {
                     "type": "LineString",
                     "coordinates": coordinates[i]
                 },
                 "properties": {
                     "title": "SAT " + str(i) + " 3dB Field of View"}
                 } for i in coordinates]

    return response.json({"type": "FeatureCollection", 'features': features})


def get_geojson_TRSP_FOV_CIRCLE():
    """
    Function to get the coordinates into a GeoJSON format
    This adds the lat and longitudes for the SAT
    Called in cesium.html

    Returns:
        object: GeoJSON
    """
    transponder_fov = dbLinkBudget.TRSP_FOV
    rows = dbLinkBudget(
        (transponder_fov.Job_ID == request.args(0)) & (transponder_fov.TRSP_ID > 0)).iterselect()
    coordinates = {}

    for row in rows:
        if (row[transponder_fov.SAT_ID], row[transponder_fov.TRSP_ID]) not in coordinates:
            coordinates[row[transponder_fov.SAT_ID], row[transponder_fov.TRSP_ID]] = []
        coordinates[row[transponder_fov.SAT_ID], row[transponder_fov.TRSP_ID]].append(
            [row[transponder_fov.LON], row[transponder_fov.LAT]])

    features = [{"type": "Feature",
                 "geometry": {
                     "type": "LineString",
                     "coordinates": coordinates[i]
                 },
                 "properties": {
                     "title": "TRSP " + str(i[1]) + " SAT" + str(i[0]) + " \n 3dB Field of View"}
                 } for i in coordinates]

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


def options_widget(field, value, **kwargs):
    return SQLFORM.widgets.options.widget(field, value, **kwargs)


def string_widget(field, value, **kwargs):
    return SQLFORM.widgets.string.widget(field, value, **kwargs)


def boolean_widget(field, value, **kwargs):
    # be careful using this; checkboxes on forms are tricky. see notes below.
    return SQLFORM.widgets.boolean.widget(field, value, **kwargs)
