# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by lbController give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
dbTest = DAL('sqlite://storage.sqlite')
dbTest.define_table('test1', Field('name', 'string'), Field('t_num'))
dbTest.define_table('testUpXcel',
                    Field('job', 'string', requires=IS_NOT_EMPTY(), unique=True),
                    Field('fileUp', 'upload', requires=IS_NOT_EMPTY(),
                          autodelete=True))  ##This is a good example to build the real excel database from
##IMPORTANT TO NOTE autodelete


# Test definition for future database
dbLinkBudget = DAL('sqlite://storage.sqlite')
dbLinkBudget.define_table('SAT_FOV',
                          Field('Job_ID', requires=IS_IN_DB(dbLinkBudget, 'Job.id')),
                          Field('SAT_ID', 'double', requires=IS_NOT_EMPTY()),
                          Field('LON', 'double', requires=IS_NOT_EMPTY()),
                          Field('LAT', 'double', requires=IS_NOT_EMPTY()), )
dbLinkBudget.define_table('TRSP_FOV',
                          Field('Job_ID', requires=IS_IN_DB(dbLinkBudget, 'Job.id')),
                          Field('SAT_ID', 'double', requires=IS_NOT_EMPTY()),
                          Field('TRSP_ID', 'double', requires=IS_NOT_EMPTY()),
                          Field('LON', 'double', requires=IS_NOT_EMPTY()),
                          Field('LAT', 'double', requires=IS_NOT_EMPTY()), )
dbLinkBudget.define_table('VSAT',
                          Field('Job_ID', requires=IS_IN_DB(dbLinkBudget, 'Job.id')),
                          Field('VSAT_ID', 'string'),  # ,unique=True),
                          Field('GPT', 'double'),
                          Field('DIAMETER', 'double'),
                          Field('POLAR', 'string', requires=IS_IN_SET(('C', 'CC'))),
                          Field('EFFICIENCY', 'double'))
dbLinkBudget.define_table('Gateway',
                          Field('Job_ID', requires=IS_IN_DB(dbLinkBudget, 'Job.id')),
                          Field('GW_ID', 'string', requires=IS_NOT_EMPTY()),  # ,unique = True),
                          Field('EIRP_MAX', 'double', requires=IS_NOT_EMPTY()),
                          Field('GT', 'double', requires=IS_NOT_EMPTY()),
                          Field('RS_MIN', 'double', requires=IS_NOT_EMPTY()),
                          Field('RS_MAX', 'double', requires=IS_NOT_EMPTY()),
                          Field('BANDWIDTH', 'double', requires=IS_NOT_EMPTY()),
                          Field('DIAMETER', 'double', requires=IS_NOT_EMPTY()),
                          Field('POLAR', 'string', requires=[IS_IN_SET(('C', 'CC')), IS_NOT_EMPTY()]),
                          Field('EFFICIENCY', 'double', requires=IS_NOT_EMPTY()))
dbLinkBudget.define_table('TRSP',
                          Field('Job_ID', requires=IS_IN_DB(dbLinkBudget, 'Job.id')),
                          Field('FWD_RTN_FLAG', 'string', requires=IS_NOT_EMPTY()),
                          Field('PAYLOAD_ID', 'string', requires=IS_NOT_EMPTY()),
                          Field('TRSP_ID', 'string', requires=IS_NOT_EMPTY()),
                          Field('SYS_TEMP', 'double', requires=IS_NOT_EMPTY()),
                          Field('CENTRAL_FQ_UP', 'double', requires=IS_NOT_EMPTY()),
                          Field('BANDWIDTH', 'double', requires=IS_NOT_EMPTY()),
                          Field('CENTRAL_FQ_DN', 'double', requires=IS_NOT_EMPTY()),
                          Field('AMP_SAT', 'double', requires=IS_NOT_EMPTY()),
                          Field('IBO', 'double', requires=IS_NOT_EMPTY()),
                          Field('BEAM_RX_ID', 'string', requires=IS_NOT_EMPTY()),
                          Field('BEAM_RX_TYPE', 'string', requires=IS_NOT_EMPTY()),
                          Field('BEAM_RX_CENTER_AZ_ANT', 'double', requires=IS_NOT_EMPTY()),
                          Field('BEAM_RX_CENTER_EL_ANT', 'double', requires=IS_NOT_EMPTY()),
                          Field('BEAM_RX_ANT_DIAM', 'double', requires=IS_NOT_EMPTY()),
                          Field('BEAM_RX_THETA_3DB', 'double', requires=IS_NOT_EMPTY()),
                          Field('BEAM_RX_EFF', 'double', requires=IS_NOT_EMPTY()),
                          Field('BEAM_RX_RADIUS', 'double', requires=IS_NOT_EMPTY()),
                          Field('BEAM_TX_ID', 'string', requires=IS_NOT_EMPTY()),
                          Field('BEAM_TX_TYPE', 'string', requires=IS_NOT_EMPTY()),
                          Field('BEAM_TX_CENTER_AZ_ANT', 'double', requires=IS_NOT_EMPTY()),
                          Field('BEAM_TX_CENTER_EL_ANT', 'double', requires=IS_NOT_EMPTY()),
                          Field('BEAM_TX_ANT_DIAM', 'double', requires=IS_NOT_EMPTY()),
                          Field('BEAM_TX_THETA_3DB', 'double', requires=IS_NOT_EMPTY()),
                          Field('BEAM_TX_EFF', 'double', requires=IS_NOT_EMPTY()),
                          Field('BEAM_TX_RADIUS', 'double', requires=IS_NOT_EMPTY()),
                          Field('MAX_GAIN_TX', 'double'),
                          Field('MAX_GAIN_RX', 'double'))
dbLinkBudget.define_table('SAT',
                          Field('Job_ID', requires=IS_IN_DB(dbLinkBudget, 'Job.id')),
                          Field('SAT_ID', 'string', requires=IS_NOT_EMPTY()),  # ,unique = True),
                          Field('NADIR_LON', 'double', requires=IS_NOT_EMPTY()),
                          Field('NADIR_LAT', 'double', requires=IS_NOT_EMPTY()),
                          Field('DISTANCE', 'double', requires=IS_NOT_EMPTY()),
                          Field('INCLINATION_ANGLE', 'double', requires=IS_NOT_EMPTY()),
                          Field('FOV_RADIUS', 'double', requires=IS_NOT_EMPTY()),
                          Field('FLAG_ASC_DESC', 'string', requires=IS_NOT_EMPTY()),
                          Field('INTERF_FLAG', 'boolean', requires=IS_NOT_EMPTY()),
                          Field('ROLL', 'double', requires=IS_NOT_EMPTY()),
                          Field('PITCH', 'double', requires=IS_NOT_EMPTY()),
                          Field('YAW', 'double', requires=IS_NOT_EMPTY()),
                          Field('PAYLOAD_ID', 'string', requires=IS_IN_DB(dbLinkBudget, dbLinkBudget.TRSP.PAYLOAD_ID)),
                          Field('NADIR_X_ECEF', 'double'),
                          Field('NADIR_Y_ECEF', 'double'),
                          Field('NADIR_Z_ECEF', 'double'),
                          Field('SAT_POS_X_ECEF', 'double'),
                          Field('SAT_POS_Y_ECEF', 'double'),
                          Field('SAT_POS_Z_ECEF', 'double'),
                          Field('NORMAL_VECT_X', 'double'),
                          Field('NORMAL_VECT_Y', 'double'),
                          Field('NORMAL_VECT_Z', 'double'))  # From a quick search online the IS_IN_DB function can't
# be in a list otherwise it won't

dbLinkBudget.SAT.PAYLOAD_ID.requires = IS_NOT_EMPTY()  # generated as a list. Futher testing required
dbLinkBudget.define_table('Job',
                          Field('job_name', 'string', requires=IS_NOT_EMPTY(), label='Name'),
                          Field('description', 'string'),
                          Field('Date', 'string', default=request.now, update=request.now, writable=False,
                                label='Upload Date'),
                          Field('file_up', 'upload', requires=IS_NOT_EMPTY(), label='File (excel spreadsheet)',
                                autodelete=True),
                          )

dbLinkBudget.define_table('Calculate',
                          Field('processed_file', 'upload', writable=False, readable=False, autodelete=True),
                          Field('simulator_mode', 'string', requires=IS_IN_SET(('FWD', 'RTN')), default='FWD',
                                label='Simulation Mode (FWD or RTN)'),

                          Field('sat_geo_params', 'boolean', label='1) Compute Satellite Geometric Parameters'),
                          Field('sat_fov', 'boolean', label='1a) Compute Satellite FOV'),
                          Field('trsp_fov', 'boolean', label='1b) Compute Transponder FOV'),
                          Field('points2trsp', 'boolean', label='2) Assign Earth points coverage to transponder(VSAT)'),
                          Field('gw2trsp', 'boolean', label='3) Assign Earth gateways to transponder (Gateway)'),
                          Field('comp_point_cover', 'boolean',
                                label='4) Compute geometric parameters for Earth points coverage (VSAT)'),
                          Field('comp_gw_cover', 'boolean',
                                label='5) Compute geometric parameters for Earth gateways (Gateway)'),
                          Field('propa_feeder_link', 'boolean',
                                label='6) Compute propagation on Feeder Link (Gateway)'),
                          Field('propa_user_link', 'boolean', label='7) Compute propagation on User Link (VSAT)'),
                          Field('sat_up_perf', 'boolean', label='8) Compute satellite uplink performances (e.g. G/T)'),
                          Field('sat_dwn_perf', 'boolean',
                                label='9) Compute satellite downlink performances (e.g. EIRP)'),
                          Field('comp_link_budget', 'boolean', label='10) Compute link budget'),
                          Field('csn0_up_flag', 'string', requires=IS_IN_SET(('To Compute', 'From File', 'Disregard')),
                                default='Disregard', label='a) C/N0up'),
                          Field('csi0_up_flag', 'string', requires=IS_IN_SET(('To Compute', 'From File', 'Disregard')),
                                default='Disregard', label='b) C/I0up'),
                          Field('csim0_flag', 'string', requires=IS_IN_SET(('To Compute', 'From File', 'Disregard')),
                                default='Disregard', label='c) C/Im0'),
                          Field('csn0_dn_flag', 'string', requires=IS_IN_SET(('To Compute', 'From File', 'Disregard')),
                                default='Disregard', label='d) C/N0dn'),
                          Field('csi0_dn_flag', 'string', requires=IS_IN_SET(('To Compute', 'From File', 'Disregard')),
                                default='Disregard', label='e) C/I0dn'),
                          Field('processed', 'boolean', default=False,
                                label='Processed? Leave this unchecked and it becomes checked when you press the Run '
                                      'button'),
                          )
# dbLinkBudget.Job.file_up.requires=IS_UPLOAD_FILENAME(extension=['xlsx','xls','xml'])
dbLinkBudget.define_table('Earth_coord_GW',
                          Field('Job_ID', requires=IS_IN_DB(dbLinkBudget, 'Job.id')),
                          Field('LON', 'double', requires=IS_NOT_EMPTY()),
                          Field('LAT', 'double', requires=IS_NOT_EMPTY()),
                          Field('ALT', 'double', requires=IS_NOT_EMPTY()),
                          Field('AVAILABILITY_UP', 'double', requires=IS_NOT_EMPTY()),
                          Field('AVAILABILITY_DN', 'double', requires=IS_NOT_EMPTY()),
                          Field('SAT_ID', 'string', requires=IS_IN_DB(dbLinkBudget, dbLinkBudget.SAT.SAT_ID)),
                          Field('PAYLOAD_ID', 'string', requires=IS_IN_DB(dbLinkBudget, dbLinkBudget.TRSP.PAYLOAD_ID)),
                          Field('TRSP_ID', 'string', requires=IS_IN_DB(dbLinkBudget, dbLinkBudget.TRSP.TRSP_ID)),
                          Field('GW_ID', 'string', requires=IS_IN_DB(dbLinkBudget, dbLinkBudget.Gateway.GW_ID)),
                          Field('POS_X_ECEF', 'double'),
                          Field('POS_Y_ECEF', 'double'),
                          Field('POS_Z_ECEF', 'double'),
                          Field('SAT_POS_X_ECEF', 'double'),
                          Field('SAT_POS_Y_ECEF', 'double'),
                          Field('SAT_POS_Z_ECEF', 'double'),
                          Field('DIST', 'double'),
                          Field('ELEVATION', 'double'),
                          Field('NADIR_X_ECEF', 'double'),
                          Field('NADIR_Y_ECEF', 'double'),
                          Field('NADIR_Z_ECEF', 'double'),
                          Field('NORMAL_VECT_X', 'double'),
                          Field('NORMAL_VECT_Y', 'double'),
                          Field('NORMAL_VECT_Z', 'double'),
                          Field('ROLL', 'double'),
                          Field('PITCH', 'double'),
                          Field('YAW', 'double'),
                          Field('AZ_SC', 'double'),
                          Field('ELEV_SC', 'double'),
                          Field('CENTRAL_FQ_DN', 'double'),
                          Field('FSL_DN', 'double'),
                          Field('POLAR', 'string'),
                          Field('DIAMETER', 'double'),
                          Field('EFFICIENCY', 'double'),
                          Field('POLAR_TILT_ANGLE', 'double'),
                          Field('PROPAG_DN', 'double'),
                          Field('BEAM_TX_CENTER_AZ_ANT', 'double'),
                          Field('BEAM_TX_CENTER_EL_ANT', 'double'),
                          Field('BEAM_TX_ANT_DIAM', 'double'),
                          Field('BEAM_TX_TYPE', 'string'),
                          Field('MAX_GAIN_TX', 'double'),
                          Field('BEAM_TX_THETA_3DB', 'double'),
                          Field('SAT_GAIN_TX', 'double'),
                          Field('IBO', 'double'),
                          Field('AMP_SAT', 'double'),
                          Field('OBO', 'double'),
                          Field('SAT_EIRP', 'double'))
dbLinkBudget.define_table('EARTH_coord_VSAT',
                          Field('Job_ID', requires=IS_IN_DB(dbLinkBudget, dbLinkBudget.Job.id)),
                          Field('LON', 'double', requires=IS_NOT_EMPTY()),
                          Field('LAT', 'double', requires=IS_NOT_EMPTY()),
                          Field('COUNTRY', 'string'),
                          Field('SEA_LAND', 'string', requires=IS_IN_SET(('SEA', 'GRD'))),
                          Field('VSAT_ID', 'string', requires=IS_IN_DB(dbLinkBudget, dbLinkBudget.VSAT.VSAT_ID)),
                          Field('ALT', 'double'),
                          Field('AVAILABILITY_UP', 'double'),
                          Field('AVAILABILITY_DN', 'double'),
                          Field('USER_NEED', 'integer'),
                          Field('SAT_ID', 'string', requires=IS_IN_DB(dbLinkBudget, dbLinkBudget.SAT.SAT_ID)),
                          Field('TRSP_ID', 'string', requires=IS_IN_DB(dbLinkBudget, dbLinkBudget.TRSP.TRSP_ID)),
                          Field('PAYLOAD_ID', 'string', requires=IS_IN_DB(dbLinkBudget, dbLinkBudget.TRSP.PAYLOAD_ID)),
                          Field('POS_X_ECEF', 'double'),
                          Field('POS_Y_ECEF', 'double'),
                          Field('POS_Z_ECEF', 'double'),
                          Field('SAT_POS_X_ECEF', 'double'),
                          Field('SAT_POS_Y_ECEF', 'double'),
                          Field('SAT_POS_Z_ECEF', 'double'),
                          Field('DIST', 'double'),
                          Field('ELEVATION', 'double'),
                          Field('NADIR_X_ECEF', 'double'),
                          Field('NADIR_Y_ECEF', 'double'),
                          Field('NADIR_Z_ECEF', 'double'),
                          Field('NORMAL_VECT_X', 'double'),
                          Field('NORMAL_VECT_Y', 'double'),
                          Field('NORMAL_VECT_Z', 'double'),
                          Field('ROLL', 'double'),
                          Field('PITCH', 'double'),
                          Field('YAW', 'double'),
                          Field('AZ_SC', 'double'),
                          Field('ELEV_SC', 'double'),
                          Field('CENTRAL_FQ_DN', 'double'),
                          Field('FSL_DN', 'double'),
                          Field('POLAR', 'string'),
                          Field('DIAMETER', 'double'),
                          Field('EFFICIENCY', 'double'),
                          Field('POLAR_TILT_ANGLE', 'double'),
                          Field('PROPAG_DN', 'double'),
                          Field('BEAM_TX_CENTER_AZ_ANT', 'double'),
                          Field('BEAM_TX_CENTER_EL_ANT', 'double'),
                          Field('BEAM_TX_ANT_DIAM', 'double'),
                          Field('BEAM_TX_TYPE', 'string'),
                          Field('POLAR_TILT_ANGLE', 'double'),
                          Field('MAX_GAIN_TX', 'double'),
                          Field('BEAM_TX_THETA_3DB', 'double'),
                          Field('POLAR_TILT_ANGLE', 'double'),
                          Field('SAT_GAIN_TX', 'double'),
                          Field('IBO', 'double'),
                          Field('AMP_SAT', 'double'),
                          Field('OBO', 'double'),
                          Field('SAT_EIRP', 'double'),
                          Field('CSIM0', 'double'),
                          Field('CSN0_DN', 'double'),
                          Field('CSI0_DN', 'double'),
                          Field('GPT', 'double'),
                          Field('SAT_GAIN_RX', 'double'),
                          Field('BEAM_RX_CENTER_EL_ANT', 'double'),
                          Field('CENTRAL_FQ_UP', 'double'),
                          Field('BEAM_RX_CENTER_AZ_ANT', 'double'),
                          Field('BEAM_RX_THETA_3DB', 'double'),
                          Field('PROPAG_UP', 'double'),
                          Field('SAT_GPT', 'double'),
                          Field('BEAM_RX_TYPE', 'string'),
                          Field('FSL_UP', 'double'),
                          Field('SYS_TEMP', 'double'),
                          Field('BEAM_RX_ANT_DIAM', 'double'),
                          Field('MAX_GAIN_RX', 'double'))
dbLinkBudget.executesql('CREATE INDEX IF NOT EXISTS VSAT_index ON EARTH_coord_VSAT (Job_ID);')
dbLinkBudget.executesql('CREATE INDEX IF NOT EXISTS GW_index ON Earth_coord_GW (Job_ID);')
