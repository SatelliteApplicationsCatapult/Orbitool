# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 17:37:52 2015

THIS LIBRARY ACTUALLY IMPORTS PROPA.DLL from CNES
refer to CNES documentation (user manual of library)

***REMOVED***
"""
import logging
logger = logging.getLogger("web2py.app.myweb2pyapplication")
logger.setLevel(logging.DEBUG)

from lbConfiguration import pathtopropa
import ctypes as p
import numpy as np
#import os

#filepath = os.path.dirname(os.path.abspath(__file__))
_lib = p.windll.LoadLibrary(pathtopropa)


# _----------------------------------------------------------------------------------------
def compute_propag(lon, lat, alt, elevation, freq, tilt_polar_angle, diameter, efficiency, availability):
    # '''
    # This function computes propagation attenuation due to rain conditions, using the CNES library available at :
    #
    # description : TODO
    # '''
    #
    # # compute propagation losses
    # # freq in MHz
    # # availability in percentage (%)
    # # vectorized
    #
    # # convert freq in GHz
    # freq = freq / 1e3
    #
    # # convert elevation in radians
    # elevation = elevation * np.pi / 180
    #
    # # compute "percentage of time"
    # time_pct = 100 - availability * 100
    #
    # # initiate values
    # vct = np.arange(0, np.size(lon), 1)
    # Agaseous = np.zeros(np.size(lon))
    # Aclouds = np.zeros(np.size(lon))
    # Iscint = np.zeros(np.size(lon))
    # Arain = np.zeros(np.size(lon))
    #
    # for ctr in vct:
    #     # Intermediate parameters computation
    #     hr = rain_height(lat[ctr], lon[ctr])
    #     R001 = rain_intensity(lat[ctr], lon[ctr], 0.01)
    #     Temp = temperature(lat[ctr], lon[ctr])
    #     ro = SWVD(lat[ctr], lon[ctr])
    #     #        WVC = IWVC(lat[ctr],lon[ctr],time_pct[ctr])
    #     LWC = LWCC(lat[ctr], lon[ctr], time_pct[ctr])
    #     Nwet = NWET(lat[ctr], lon[ctr])
    #
    #     # GASEOUS ATTENUATION
    #     Agaseous[ctr] = gaseous_attenuation(freq[ctr], elevation[ctr], Temp, ro);
    #
    #     # GASEOUS ATTENUATION EXCEEDED FOR availability% OF THE TIME
    #     #        Agaseous = gaseous_attenuation_exc(freq[ctr],elevation[ctr],Temp,WVC,ro)
    #
    #     # CLOUD ATTENUATION EXCEEDED FOR availability% OF THE TIME
    #     Aclouds[ctr] = cloud_attenuation(freq[ctr], elevation[ctr], LWC)
    #
    #     # IMPAIRMENT DUE to SCINTILLATION EXCEEDED FOR availability% OF THE TIME
    #     Iscint[ctr] = scintillation(Nwet, freq[ctr], elevation[ctr], time_pct[ctr], alt[ctr], efficiency[ctr],
    #                                 diameter[ctr])
    #
    #     # RAIN ATTENUATION EXCEEDED FOR availability% OF THE TIME
    #     Arain[ctr] = rain_attenuation(lat[ctr], freq[ctr], elevation[ctr], time_pct[ctr], alt[ctr], hr, R001,
    #                                   tilt_polar_angle[ctr])
    #
    # # A TOTAL
    #
    # Atot = Agaseous + np.sqrt((Aclouds + Arain) ** 2 + Iscint ** 2)
    # logger.error('Atot')
    # logger.error(Atot)
    # for the moment : bypass function (wait fro CNES library update)
    Atot = np.zeros_like(lon)
    return Atot


# _----------------------------------------------------------------------------------------
# -------------------------------------------------------------------
# NWET
_lib.NWET.restype = p.c_double
_lib.NWET.argtypes = [p.c_double, p.c_double]


def NWET(lat, lon):
    return _lib.NWET(lat, lon)


# -------------------------------------------------------------------


# -------------------------------------------------------------------
# rain_height
_lib.rain_height.restype = p.c_double
_lib.rain_height.argtypes = [p.c_double, p.c_double]


def rain_height(lat, lon):
    return _lib.rain_height(lat, lon)


# -------------------------------------------------------------------

# -------------------------------------------------------------------
# temperature
_lib.temperature.restype = p.c_double
_lib.temperature.argtypes = [p.c_double, p.c_double]


def temperature(lat, lon):
    return _lib.temperature(lat, lon)


# -------------------------------------------------------------------

# -------------------------------------------------------------------
# rain intensity
_lib.rain_intensity.restype = p.c_double
_lib.rain_intensity.argtypes = [p.c_double, p.c_double, p.c_double]


def rain_intensity(lat, lon, p):
    return _lib.rain_intensity(lat, lon, p)


# -------------------------------------------------------------------

# -------------------------------------------------------------------
# rain_probability
_lib.rain_probability.restype = p.c_double
_lib.rain_probability.argtypes = [p.c_double, p.c_double]


def rain_probability(lat, lon):
    return _lib.rain_probability(lat, lon)


# -------------------------------------------------------------------

# -------------------------------------------------------------------
# LWCC
_lib.LWCC.restype = p.c_double
_lib.LWCC.argtypes = [p.c_double, p.c_double, p.c_double]


def LWCC(lat, lon, p):
    return _lib.LWCC(lat, lon, p)


# -------------------------------------------------------------------


# -------------------------------------------------------------------
# IWVC
_lib.IWVC.restype = p.c_double
_lib.IWVC.argtypes = [p.c_double, p.c_double, p.c_double]


def IWVC(lat, lon, p):
    return _lib.IWVC(lat, lon, p)


# -------------------------------------------------------------------

# -------------------------------------------------------------------
# SWVD
_lib.SWVD.restype = p.c_double
_lib.SWVD.argtypes = [p.c_double, p.c_double]


def SWVD(lat, lon):
    return _lib.SWVD(lat, lon)


# -------------------------------------------------------------------

# -------------------------------------------------------------------
# gaseous_attenuation
_lib.gaseous_attenuation.restype = p.c_double
_lib.gaseous_attenuation.argtypes = [p.c_double, p.c_double, p.c_double, p.c_double]


def gaseous_attenuation(f, E, Temp, ro):
    return _lib.gaseous_attenuation(f, E, Temp, ro)


# -------------------------------------------------------------------

# -------------------------------------------------------------------
# gaseous_attenuation_exc
_lib.gaseous_attenuation_exc.restype = p.c_double
_lib.gaseous_attenuation_exc.argtypes = [p.c_double, p.c_double, p.c_double, p.c_double, p.c_double]


def gaseous_attenuation_exc(f, E, Temp, WVC, ro):
    return _lib.gaseous_attenuation_exc(f, E, Temp, WVC, ro)


# -------------------------------------------------------------------

# -------------------------------------------------------------------
# cloud_attenuation
_lib.cloud_attenuation.restype = p.c_double
_lib.cloud_attenuation.argtypes = [p.c_double, p.c_double, p.c_double]


def cloud_attenuation(f, E, L):
    return _lib.cloud_attenuation(f, E, L)


# -------------------------------------------------------------------

# -------------------------------------------------------------------
# rain_attenuation
_lib.rain_attenuation.restype = p.c_double
_lib.rain_attenuation.argtypes = [p.c_double, p.c_double, p.c_double, p.c_double, \
                                  p.c_double, p.c_double, p.c_double, p.c_double]


def rain_attenuation(lat, f, E, p, hs, hr, R001, to):
    return _lib.rain_attenuation(lat, f, E, p, hs, hr, R001, to)


# -------------------------------------------------------------------

# -------------------------------------------------------------------
# scintillation
_lib.scintillation.restype = p.c_double
_lib.scintillation.argtypes = [p.c_double, p.c_double, p.c_double, p.c_double, \
                               p.c_double, p.c_double, p.c_double]


def scintillation(Nwet, f, E, p, hs, eta, D):
    return _lib.scintillation(Nwet, f, E, p, hs, eta, D)

# -------------------------------------------------------------------
