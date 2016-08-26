# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
from excelHandling import *
import os

def index():
    import subprocess
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    return auth.wiki()
    if you need a simple wiki simply replace the two lines below with:

    """
    return dict(message=T('Welcome to the Link Budget Server!'))

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

def job_up():                                 #Input Form page
    session.job = ""
    record = dbLinkBudget.Job(request.args(0))   #Required if page used to update records
    dbLinkBudget.Job.Date.readable = False       #SQL form formatting
    form = SQLFORM(dbLinkBudget.Job,record, deletable=True,
                  upload=URL('download'),formstyle='bootstrap3_inline')
    if form.process().accepted:
        session.job = form.vars.job_name
        add_excel_2_db()
    return dict(form = form)

def test_crud():       #Test Function used to test code before major use
    return dict(a=0)

def add_excel_2_db():       #Function used to insert excel dictionary into database
    import numpy as np

    file = dbLinkBudget.Job(dbLinkBudget.Job.job_name==session.job).file_up       #Find uploaded file
    job_id = dbLinkBudget.Job(dbLinkBudget.Job.job_name==session.job).id
    [SAT_dict, TRSP_dict, VSAT_dict, EARTH_COORD_GW_dict,  GW_dict, EARTH_COORD_VSAT_dict, display_dict_VSAT] = load_objects_from_xl(os.path.join(request.folder,'uploads',file))
    read_array_to_db(dbLinkBudget.VSAT,VSAT_dict)
    read_array_to_db(dbLinkBudget.Gateway,GW_dict)
    read_array_to_db(dbLinkBudget.TRSP,TRSP_dict)
    read_array_to_db(dbLinkBudget.SAT,SAT_dict)
    read_array_to_db(dbLinkBudget.Earth_coord_GW,EARTH_COORD_GW_dict,job_id)
    read_array_to_db(dbLinkBudget.EARTH_coord_VSAT,EARTH_COORD_VSAT_dict,job_id)
    #SAT_dict = compute_sat_params(SAT_dict)
    redirect(URL('view_db',args = job_id))

def read_array_to_db(db, ordDict,job_id=0):     #Used to read in dictionaries which contain numpy arrays created when reading excel file
    import numpy as np                         #The DAL insert statement can handle dictionaries but not arrays
    temp = ordDict.fromkeys(ordDict,0)
    if job_id <> 0:    #Check for tables which require records to be assigned with job_id number
        temp['Job_ID'] = job_id
    for i in range(ordDict.values()[0].size):
        for j in range(len(ordDict.keys())):
            temp[ordDict.keys()[j]] = ordDict.values()[j][i]
        db.update_or_insert(**temp)          #Update/Insert state used to create new database records

def search_db():      #Search database page
    import json
    job = json.dumps(dbLinkBudget(dbLinkBudget.Job).select().as_list(),default=json_serial)  #Formatting need to interface with JQuery Datatables
    return dict(job=XML(job))

def view_db():      #View database page
    import json
    job = json.dumps(dbLinkBudget(dbLinkBudget.Job).select().as_list(),default=json_serial)    #default json.dumps specificed
    gw=[]
    vsat=[]
    sat = []
    for row in dbLinkBudget(dbLinkBudget.Earth_coord_GW.Job_ID==request.args(0)).iterselect(groupby = 'GW_ID'):
        gw.extend(dbLinkBudget(dbLinkBudget.Gateway.GW_ID==row['GW_ID']).select().as_list())

    for row in dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.Job_ID==request.args(0)).iterselect(groupby = 'VSAT_ID'): #groupby only selects the distinct values from DB
            vsat.extend(dbLinkBudget(dbLinkBudget.VSAT.VSAT_ID==row['VSAT_ID']).select().as_list())

    for row in dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.Job_ID==request.args(0)).iterselect(groupby = 'SAT_ID'): #groupby only selects the distinct values from DB
            sat.extend(dbLinkBudget(dbLinkBudget.SAT.SAT_ID==row['SAT_ID']).select().as_list())
    record = dbLinkBudget.Job(request.args(0))
    dbLinkBudget.Job.Date.readable=False
    form = SQLFORM(dbLinkBudget.Job,record, deletable=True,formstyle='table3cols',submit_button='Update')
    response.flash=form.vars.job_name
    if form.process().accepted:
        session.job = form.vars.job_name
        add_excel_2_db()
    return dict(job=XML(job),vsat=XML(json.dumps(vsat)),gw = XML(json.dumps(gw)),sat=json.dumps(sat),form=form)

def json_serial(obj):    #function needed to serialise the date field for json output
    from datetime import datetime
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj,datetime):
        serial = obj.strftime("%d-%m-%Y  %H:%M")
        return serial
    raise TypeError ("Type not serializable")

def download():
    return response.download(request, dbLinkBudget)

def create_download():
    rowt = dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.Job_ID==request.args(0)).iterselect("PAYLOAD_ID","AVAILABILITY_DN","TRSP_ID","LON","LAT","AVAILABILITY_UP","SAT_ID","SAT_EIRP","ALT","VSAT_ID").first().as_dict()
    temp = dict.fromkeys(rowt["_extra"])
    for key in temp.keys():
        temp[key]=[]
    for row in dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.Job_ID==request.args(0)).iterselect("PAYLOAD_ID","AVAILABILITY_DN","TRSP_ID","LON","LAT","AVAILABILITY_UP","SAT_ID","SAT_EIRP","ALT","VSAT_ID"):
        for key in temp.keys():
            temp[key].append(row["_extra"][key])
    filename = request.args(0) + ".xlsx"
    filepath = os.path.join(request.folder,'uploads',filename)
    create_saving_worksheet(filepath, temp, "Output")
    stream = open(filepath, 'rb')
    dbLinkBudget(dbLinkBudget.Job.id==request.args(0)).update(processed_file=dbLinkBudget.Job.processed_file.store(stream, filepath))
    os.remove(filepath)
    redirect(URL('download',args = dbLinkBudget.Job(dbLinkBudget.Job.id==request.args(0)).processed_file))

def process():   #Process job function
    import subprocess   #TODO : extend to use input checklist and chose certain jobs, Damian Code required
    cfile = os.path.join(request.folder,'static',"propa2")
    for row in dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.Job_ID == request.args(0)).iterselect():
        lon = row.LON
        lat = row.LAT
        proc = subprocess.Popen([cfile,str(lon),str(lat),],stdout=subprocess.PIPE)
        (out,err)=proc.communicate()
        dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.id == row.id).update(SAT_EIRP=out)
    dbLinkBudget(dbLinkBudget.Job.id == request.args(0)).update(processed=True)
    redirect(URL('view_db',args = request.args(0)))

def cesium():
    return dict(a = 1)

def get_geojson():   #Get geojson function called for cesium to query db and build json output
    import json
    rows= dbLinkBudget(dbLinkBudget.EARTH_coord_VSAT.Job_ID==request.args(0)).iterselect()  #iterselect used to save on memory resources
                                                                                            #TODO : test if iterselect is better than regular select, time and memory resources.
    features= [{"type": "Feature",
                "geometry": {
                "type" : "Point",
                "coordinates" : [r[dbLinkBudget.EARTH_coord_VSAT.LON],r[dbLinkBudget.EARTH_coord_VSAT.LAT]]
                },
                "properties": {
                    "title": ["Lon: " + str(r[dbLinkBudget.EARTH_coord_VSAT.LON])," Lat: " +str(r[dbLinkBudget.EARTH_coord_VSAT.LAT])],
                    "Job ID" : r[dbLinkBudget.EARTH_coord_VSAT.Job_ID],
                    "EIRP" : r[dbLinkBudget.EARTH_coord_VSAT.SAT_EIRP]
                }
            }for r in rows]  #TODO : Extend to include more information form database
    return response.json({"type": "FeatureCollection", 'features': features})

def get_geojson_gw():    #Get geojson function called for cesium to query db and build json output
    import json
    rows= dbLinkBudget(dbLinkBudget.Earth_coord_GW.Job_ID==request.args(0)).iterselect()

    features= [{"type": "Feature",
                "geometry": {
                "type" : "Point",
                "coordinates" : [r[dbLinkBudget.Earth_coord_GW.LON],r[dbLinkBudget.Earth_coord_GW.LAT]]
                },
                "properties": {
                    "title": "Gateway",
                    "Job ID" : r[dbLinkBudget.Earth_coord_GW.Job_ID],
                    "Gateway ID" : r[dbLinkBudget.Earth_coord_GW.GW_ID],
                    "EIRP Max" : dbLinkBudget.Gateway(dbLinkBudget.Gateway.GW_ID==r[dbLinkBudget.Earth_coord_GW.GW_ID]).EIRP_MAX,
                    "Bandwidth": dbLinkBudget.Gateway(dbLinkBudget.Gateway.GW_ID==r[dbLinkBudget.Earth_coord_GW.GW_ID]).BANDWIDTH,
                    "Diameter": dbLinkBudget.Gateway(dbLinkBudget.Gateway.GW_ID==r[dbLinkBudget.Earth_coord_GW.GW_ID]).DIAMETER
                }
            }for r in rows]
    return response.json({"type": "FeatureCollection", 'features': features})
