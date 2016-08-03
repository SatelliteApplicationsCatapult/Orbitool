# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
from functest import *
import os

def index():
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


def display_form():
    session.job = ""
    record = dbTest.testUpXcel(request.args(0))
    form = SQLFORM(dbTest.testUpXcel,record, deletable=True,
                  upload=URL('download'))

    if form.process().accepted:
            session.job = form.vars.job
            redirect(URL('test_func'))

    return dict(form = form)

def job_up():
    session.job = ""
    record = dbLinkBudget.Job(request.args(0))
    form = SQLFORM(dbLinkBudget.Job,record, deletable=True,
                  upload=URL('download'),formstyle='bootstrap3_inline')

    if form.process().accepted:
            session.job = form.vars.job_name
            redirect(URL('test_func'))

    return dict(form = form)

def test_crud():
    from gluon.tools import Crud
    crud = Crud(dbLinkBudget)
    crud.settings.formstyle = "bootstrap3_inline"
    return dict(form = crud.update(dbLinkBudget.Job,request.args(0)))

def test_func():
    import numpy as np

    file = dbLinkBudget.Job(dbLinkBudget.Job.job_name==session.job).file_up
    [SAT_dict, TRSP_dict, VSAT_dict, EARTH_COORD_GW_dict,  GW_dict, EARTH_COORD_VSAT_dict, display_dict_VSAT] = load_objects_from_xl(os.path.join(request.folder,'uploads',file))
    dbLinkBudget.VSAT.update_or_insert(**VSAT_dict)
    dbLinkBudget.Gateway.update_or_insert(**GW_dict)
    read_array_to_db(dbLinkBudget.TRSP,TRSP_dict)
    read_array_to_db(dbLinkBudget.SAT,SAT_dict)
    #SAT_dict = compute_sat_params(SAT_dict)
    return dict(SAT_dict=VSAT_dict)

def user_choice():
    record = dbTest.testUpXcel(request.args(0))
    form = SQLFORM(dbTest.testUpXcel,record, deletable=True,
                  upload=URL('download'))
    extra = TR(LABEL("HELLO WOrld I agree"), INPUT(_name='play',value=False,_type='checkbox'))
    form[0].insert(-1,extra)
    if form.process(onvalidation=process_input):
        session.flash = form.vars.name
    return dict(form = form)

def process_input(form):
    session.flash = form.vars.job
    file = dbTest.testUpXcel(dbTest.testUpXcel.job==form.vars.job).fileUp
    [SAT_dict, TRSP_dict, VSAT_dict, EARTH_COORD_GW_dict,  GW_dict, EARTH_COORD_VSAT_dict, display_dict_VSAT] = load_objects_from_xl(os.path.join(request.folder,'uploads',file))
    

def read_array_to_db(db, ordDict):
    import numpy as np
    temp = ordDict.fromkeys(ordDict,0)
    for i in range(ordDict.values()[0].size):
        for j in range(len(ordDict.keys())):
            temp[ordDict.keys()[j]] = ordDict.values()[j][i]
        db.update_or_insert(**temp)
    return 0

def download():
    return response.download(request, dbTest)
