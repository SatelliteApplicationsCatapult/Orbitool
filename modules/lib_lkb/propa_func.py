# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 17:37:52 2015

THIS LIBRARY ACTUALLY IMPORTS PROPA.DLL from CNES
refer to CNES documentation (user manual of library)

***REMOVED***
"""

import ctypes as p
import os
import config
import subprocess
filepath = os.path.dirname(os.path.abspath(__file__)) #current directory
#_lib = p.windll.LoadLibrary(filepath + '\\propa.dll') #use this for shared library
cfile = os.path.join(config.pathtopropadir, 'propa/', "propaexec")

#-------------------------------------------------------------------
# NWET
_lib.NWET.restype                         =   p.c_double
_lib.NWET.argtypes                        =   [p.c_double, p.c_double]

def NWET(lat,lon):
    return _lib.NWET(lat, lon)
#-------------------------------------------------------------------


#-------------------------------------------------------------------
# rain_height
def rain_height(lat,lon):
    proc = subprocess.Popen([cfile, "--operation", "rain_height", "--lon", str(lon), "--lat", str(lat), ],
                            stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# temperature
def temperature(lat,lon):
    proc = subprocess.Popen([cfile, "--operation", "temperature", "--lon", str(lon), "--lat", str(lat), ],stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# rain intensity
def rain_intensity(lat,lon,p):
    proc = subprocess.Popen([cfile, "--operation", "rain_intensity", "--lon", str(lon), "--lat", str(lat), "--p" str(p) ],
                            stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out
#-------------------------------------------------------------------
    
#-------------------------------------------------------------------
# rain_probability
def rain_probability(lat,lon):
    proc = subprocess.Popen([cfile, "--operation", "rain_probability", "--lon", str(lon), "--lat", str(lat), ],
                            stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# LWCC
def LWCC(lat,lon,p):
    proc = subprocess.Popen(
        [cfile, "--operation", "LWCC", "--lon", str(lon), "--lat", str(lat), "--p" str(p)],
        stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out
#-------------------------------------------------------------------
    

#-------------------------------------------------------------------
# IWVC
def IWVC(lat,lon,p):
    proc = subprocess.Popen(
        [cfile, "--operation", "IWVC", "--lon", str(lon), "--lat", str(lat), "--p" str(p)],
        stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out
#-------------------------------------------------------------------
    
#-------------------------------------------------------------------
# SWVD
def SWVD(lat,lon):
    proc = subprocess.Popen([cfile, "--operation", "SWVD", "--lon", str(lon), "--lat", str(lat), ],
                            stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out
#-------------------------------------------------------------------
    
#-------------------------------------------------------------------
# gaseous_attenuation
def gaseous_attenuation(f,E, Temp, ro):
    proc = subprocess.Popen([cfile, "--operation", "gaseous_attenuation", "--freq", str(f), "--elev", str(E), "--T", str(Temp), "--ro", str(ro),],
                            stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out
#-------------------------------------------------------------------
    
#-------------------------------------------------------------------
# gaseous_attenuation_exc
def gaseous_attenuation_exc(f,E, Temp, WVC, ro):
    proc = subprocess.Popen(
        [cfile, "--operation", "gaseous_attenuation_exc", "--freq", str(f), "--elev", str(E), "--T", str(Temp), "--iwvc", str(WVC), "--ro",
         str(ro), ],
        stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out
#-------------------------------------------------------------------
    
#-------------------------------------------------------------------
# cloud_attenuation
def cloud_attenuation(f, E, L):
    proc = subprocess.Popen(
        [cfile, "--operation", "gaseous_attenuation", "--freq", str(f), "--elev", str(E), "--lwcc", str(L),],
        stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out
#-------------------------------------------------------------------
    
#-------------------------------------------------------------------
# rain_attenuation
def rain_attenuation(lat, f, E, p, hs, hr, R001, to):
    proc = subprocess.Popen(
        [cfile, "--operation", "rain_attenuation", "--lat", str(lat), "--freq", str(f), "--elev", str(E), "--p", str(p),
         "--s_height", str(hs),"--r_height", str(hr),"--R001", str(R001),"--to", str(to),],
        stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# scintillation
def scintillation(Nwet, f, E, p, hs, eta, D):
    proc = subprocess.Popen(
        [cfile, "--operation", "rain_attenuation", "--nwet", str(Nwet), "--freq", str(f), "--elev", str(E), "--p", str(p),
         "--s_height", str(hs), "--ant_eff", str(eta), "--ant_diam", str(D), ],
        stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return out
#-------------------------------------------------------------------

