# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is the Link Budget Controller
# -------------------------------------------------------------------------
from excelHandling import *

from gluon import *

import os

response.title = 'Link Budget Calculator'


def index():
    """ Home Page """
    return dict(message=T('Multi-Mission Satellite Link Budget Analysis Framework'))


def about():
    """ About page """
    return dict(message=T('About'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


def input():
    """ Input form """
    session.job = ""
    record = dbLinkBudget.Job(request.args(0))
    dbLinkBudget.Job.Date.readable = False
    form = SQLFORM(dbLinkBudget.Job, record, deletable=False,
                   upload=URL('download'), formstyle='bootstrap3_stacked')
    if form.process().accepted:
        session.job = form.vars.job_name
        add_excel_2_db()
    return dict(form=form)


def test_crud():
    """ Test Function used to test code before major use """
    return dict(a=0)


def select():
    """  Page for selecting which upload to work on  """
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
    dbLinkBudget.Job.job_name.writable = True
    form = SQLFORM(dbLinkBudget.Job, record, deletable=True, formstyle='table3cols', submit_button='Update')
    form.add_button('Back', URL('select'))
    if form.process().accepted:
        session.flash = "%s) %s has been updated" % (form.vars.id, form.vars.job_name)
        if form.deleted:
            session.flash = "%s) %s has been deleted" % (form.vars.id, form.vars.job_name)
            redirect(URL('select'))
        else:
            session.job = form.vars.job_name
            add_excel_2_db()
    return dict(job=XML(job), vsat=XML(json.dumps(vsat)), gw=XML(json.dumps(gw)), sat=XML(json.dumps(sat)), trsp=XML(json.dumps(trsp)), form=form)


def add_excel_2_db():
    """
    Function used to insert excel dictionary into database

    """
    file = dbLinkBudget.Job(dbLinkBudget.Job.job_name == session.job).file_up  # Find uploaded file
    job_id = dbLinkBudget.Job(dbLinkBudget.Job.job_name == session.job).id
    [SAT_dict, TRSP_dict, VSAT_dict, EARTH_COORD_GW_dict, GW_dict, EARTH_COORD_VSAT_dict,
     display_dict_VSAT] = load_objects_from_xl(os.path.join(request.folder, 'uploads', file))
    read_array_to_db(dbLinkBudget.VSAT, VSAT_dict)
    read_array_to_db(dbLinkBudget.Gateway, GW_dict)
    read_array_to_db(dbLinkBudget.TRSP, TRSP_dict)
    read_array_to_db(dbLinkBudget.SAT, SAT_dict)
    read_array_to_db(dbLinkBudget.Earth_coord_GW, EARTH_COORD_GW_dict, job_id)
    read_array_to_db(dbLinkBudget.EARTH_coord_VSAT, EARTH_COORD_VSAT_dict, job_id)
    # SAT_dict = compute_sat_params(SAT_dict)
    redirect(URL('update', args=job_id))


def read_array_to_db(db, ordDict, job_id=0):
    """
    Used to read in dictionaries which contain
    numpy arrays created when reading excel file

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
        db.update_or_insert(**temp)  # Update/Insert state used to create new database records


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

    Returns:
        object: 
    """
    rowt = dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.Job_ID == request.args(0)).iterselect("PAYLOAD_ID",
                                                                                            "AVAILABILITY_DN",
                                                                                            "TRSP_ID", "LON", "LAT",
                                                                                            "AVAILABILITY_UP", "SAT_ID",
                                                                                            "SAT_EIRP", "ALT",
                                                                                            "VSAT_ID").first().as_dict()
    temp = dict.fromkeys(rowt["_extra"])
    for key in temp.keys():
        temp[key] = []
    for row in dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.Job_ID == request.args(0)).iterselect("PAYLOAD_ID",
                                                                                                "AVAILABILITY_DN",
                                                                                                "TRSP_ID", "LON", "LAT",
                                                                                                "AVAILABILITY_UP",
                                                                                                "SAT_ID", "SAT_EIRP",
                                                                                                "ALT", "VSAT_ID"):
        for key in temp.keys():
            temp[key].append(row["_extra"][key])
    filename = request.args(0) + ".xlsx"
    filepath = os.path.join(request.folder, 'uploads', filename)
    create_saving_worksheet(filepath, temp, "Output")
    stream = open(filepath, 'rb')
    dbLinkBudget(dbLinkBudget.Job.id == request.args(0)).update(
        processed_file=dbLinkBudget.Job.processed_file.store(stream, filepath))
    os.remove(filepath)
    redirect(URL('download', args=dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).processed_file))


def run():
    """
    This runs the processing of the excel file.
    Currently asks which propagation library is being used.
    Adds EIRP values
    Updates 'processed' checkbox.

    Returns:
        Refreshes the update page

    """
    import subprocess  # TODO : extend to use input checklist and chose certain jobs, Damian Code required
    import config
    if dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).propaLib == 'CNES':
        cfile = os.path.join(config.pathtopropadir, 'propa/dist/Debug/GNU-Linux/', "propa")
    elif dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0)).propaLib == 'OTHER1':
        cfile = os.path.join(config.pathtopropadir, 'propa/dist/Debug/GNU-Linux/', "propa")
    else:
        cfile = os.path.join(config.pathtopropadir, 'propa/dist/Debug/GNU-Linux/', "propa")
    for row in dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.Job_ID == request.args(0)).iterselect():
        lon = row.LON
        lat = row.LAT
        proc = subprocess.Popen([cfile, str(lon), str(lat), ], stdout=subprocess.PIPE)  # runs propa
        (out, err) = proc.communicate()
        dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.id == row.id).update(SAT_EIRP=out)
    dbLinkBudget(dbLinkBudget.Job.id == request.args(0)).update(processed=True)
    redirect(URL('update', args=request.args(0)))


def cesium():
    """    Cesium viewing page cesium.html    """
    return dict(a=1)


def copy():
    """
    Function for a copy button on update.html
    Need to change it to make a new file and ID otherwise there's no point
    """
    import os
    a = dbLinkBudget.Job(dbLinkBudget.Job.id == request.args(0))
    #fileuppath = os.path.join('/home/www-data/web2py/applications/linkbudgetweb/uploads/', a.file_up)
    filename, stream = dbLinkBudget.Job.file_up.retrieve(a.file_up)
    dbLinkBudget.Job.insert(job_name= '%s_copy' % (a.job_name),
                            Date = request.now,
                            file_up = dbLinkBudget.Job.file_up.store(stream, filename), #this needs to be renamed
                            simulator_mode = a.simulator_mode,
                            propaLib = a.propaLib,
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

def get_geojson():
    """
    Function to get the coordinates into a GeoJSON format
    This adds the lat and longitude for the User Terminals
    Called in cesium.html
    TODO : test if iterselect is better than regular select, time and memory resources.

    Returns:
        object:
    """
    rows = dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.Job_ID == request.args(0)).iterselect()
    features = [{"type": "Feature",
                 "geometry": {
                     "type": "Point",
                     "coordinates": [r[dbLinkBudget.EARTH_coord_VSAT.LON], r[dbLinkBudget.EARTH_coord_VSAT.LAT]]
                 },
                 "properties": {
                     "title": ["Lon: " + str(r[dbLinkBudget.EARTH_coord_VSAT.LON]),
                               " Lat: " + str(r[dbLinkBudget.EARTH_coord_VSAT.LAT])],
                     "Job ID": r[dbLinkBudget.EARTH_coord_VSAT.Job_ID],
                     "EIRP": r[dbLinkBudget.EARTH_coord_VSAT.SAT_EIRP]
                 }
                 } for r in rows]  # TODO : Extend to include more information form database
    return response.json({"type": "FeatureCollection", 'features': features})


def get_geojson_gw():
    """
    Function to get the coordinates into a GeoJSON format
    This adds the lat and longitudes for the gateways
    Called in cesium.html

    Returns:
        object: 
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
                         dbLinkBudget.Gateway.GW_ID == r[dbLinkBudget.Earth_coord_GW.GW_ID]).DIAMETER
                 }
                 } for r in rows]
    return response.json({"type": "FeatureCollection", 'features': features})
