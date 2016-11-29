# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 17:37:52 2015

THIS LIBRARY ACTUALLY IMPORTS PROPA.DLL from CNES
refer to CNES documentation (user manual of library)

***REMOVED***
"""

import ctypes as p
import os
filepath = os.path.dirname(os.path.abspath(__file__)) #current directory
_lib = p.windll.LoadLibrary(filepath + '\\propa.dll')


#-------------------------------------------------------------------
# NWET
_lib.NWET.restype                         =   p.c_double
_lib.NWET.argtypes                        =   [p.c_double, p.c_double]

def NWET(lat,lon):
    return _lib.NWET(lat, lon)
#-------------------------------------------------------------------


#-------------------------------------------------------------------
# rain_height
_lib.rain_height.restype                  =   p.c_double
_lib.rain_height.argtypes                 =   [p.c_double, p.c_double]

def rain_height(lat,lon):
    return _lib.rain_height(lat, lon)
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# temperature
_lib.temperature.restype                  =   p.c_double
_lib.temperature.argtypes                 =   [p.c_double, p.c_double]

def temperature(lat,lon):
    return _lib.temperature(lat, lon)
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# rain intensity
_lib.rain_intensity.restype               =   p.c_double
_lib.rain_intensity.argtypes              =   [p.c_double, p.c_double, p.c_double]

def rain_intensity(lat,lon,p):
    return _lib.rain_intensity(lat, lon, p)
#-------------------------------------------------------------------
    
#-------------------------------------------------------------------
# rain_probability
_lib.rain_probability.restype             =   p.c_double
_lib.rain_probability.argtypes            =   [p.c_double, p.c_double]

def rain_probability(lat,lon):
    return _lib.rain_probability(lat, lon)
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# LWCC
_lib.LWCC.restype                         =   p.c_double
_lib.LWCC.argtypes                        =   [p.c_double, p.c_double, p.c_double]

def LWCC(lat,lon,p):
    return _lib.LWCC(lat, lon, p)
#-------------------------------------------------------------------
    

#-------------------------------------------------------------------
# IWVC
_lib.IWVC.restype                         =   p.c_double
_lib.IWVC.argtypes                        =   [p.c_double, p.c_double, p.c_double]

def IWVC(lat,lon,p):
    return _lib.IWVC(lat, lon, p)
#-------------------------------------------------------------------
    
#-------------------------------------------------------------------
# SWVD
_lib.SWVD.restype                         =   p.c_double
_lib.SWVD.argtypes                        =   [p.c_double, p.c_double]

def SWVD(lat,lon):
    return _lib.SWVD(lat, lon)
#-------------------------------------------------------------------
    
#-------------------------------------------------------------------
# gaseous_attenuation
_lib.gaseous_attenuation.restype          =   p.c_double
_lib.gaseous_attenuation.argtypes         =   [p.c_double, p.c_double, p.c_double, p.c_double]

def gaseous_attenuation(f,E, Temp, ro):
    return _lib.gaseous_attenuation(f,E, Temp, ro)
#-------------------------------------------------------------------
    
#-------------------------------------------------------------------
# gaseous_attenuation_exc
_lib.gaseous_attenuation_exc.restype      =   p.c_double
_lib.gaseous_attenuation_exc.argtypes     =   [p.c_double, p.c_double, p.c_double, p.c_double, p.c_double]

def gaseous_attenuation_exc(f,E, Temp, WVC, ro):
    return _lib.gaseous_attenuation_exc(f,E, Temp, WVC, ro)
#-------------------------------------------------------------------
    
#-------------------------------------------------------------------
# cloud_attenuation
_lib.cloud_attenuation.restype            =   p.c_double
_lib.cloud_attenuation.argtypes           =   [p.c_double, p.c_double, p.c_double]

def cloud_attenuation(f, E, L):
    return _lib.cloud_attenuation(f, E, L)
#-------------------------------------------------------------------
    
#-------------------------------------------------------------------
# rain_attenuation
_lib.rain_attenuation.restype             =   p.c_double
_lib.rain_attenuation.argtypes            =   [p.c_double, p.c_double, p.c_double, p.c_double, \
                                               p.c_double, p.c_double, p.c_double, p.c_double]        
def rain_attenuation(lat, f, E, p, hs, hr, R001, to):
    return _lib.rain_attenuation(lat, f, E, p, hs, hr, R001, to)
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# scintillation
_lib.scintillation.restype                =   p.c_double
_lib.scintillation.argtypes               =   [p.c_double, p.c_double, p.c_double, p.c_double, \
                                               p.c_double, p.c_double, p.c_double]        
def scintillation(Nwet, f, E, p, hs, eta, D):
    return _lib.scintillation(Nwet, f, E, p, hs, eta, D)
#-------------------------------------------------------------------

