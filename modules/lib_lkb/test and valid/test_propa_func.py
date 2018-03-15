# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 21:28:06 2015

*REMOVED*
"""

from sys import path

path.append("../../lib_lkb/")

from propa_func import *
import numpy as np

lat = 0.0  # Latitude (°)
lon = 0.0  # Logitude (°)

hs = 0.0  # Earth station altitude (km)
E = 33.0 * np.pi / 180  # Link elevation angle (°)

f = 20.0  # Link frequency (GHz)
to = 45.0  # Tilt polarization angle (°)

D = 2.0  # Earth station antenna diameter (m)
eta = 70  # Earth station antenna efficiency

p = 0.1  # Percentage of the time

# Intermediate parameters computation
hr = rain_height(lat, lon)
R001 = rain_intensity(lat, lon, 0.01)
Temp = temperature(lat, lon)
ro = SWVD(lat, lon)
WVC = IWVC(lat, lon, p)
LWC = LWCC(lat, lon, p)
Nwet = NWET(lat, lon)

# GASEOUS ATTENUATION
Agaseous = gaseous_attenuation(f, E, Temp, ro);
# print("\nGaseous attenuation = %.2lf dB\n",Agaseous);

# GASEOUS ATTENUATION EXCEEDED FOR p% OF THE TIME
Agaseous = gaseous_attenuation_exc(f, E, Temp, WVC, ro);
# print("\nGaseous attenuation exceeded for %.2lf %% of the time = %.2lf dB\n",p,Agaseous);

# CLOUD ATTENUATION EXCEEDED FOR p% OF THE TIME
Aclouds = cloud_attenuation(f, E, LWC);
# print("\nClouds attenuation exceeded for %.2lf %% of the time = %.2lf dB\n",p,Aclouds);

# IMPAIRMENT DUE TO SCINTILLATION EXCEEDED FOR p% OF THE TIME
Iscint = scintillation(Nwet, f, E, p, hs, eta, D);
# print("\nScintillation impairment exceeded for %.2lf %% of the time = %.2lf dB\n",p,Iscint);

# RAIN ATTENUATION EXCEEDED FOR p% OF THE TIME
Arain = rain_attenuation(lat, f, E, p, hs, hr, R001, to);
# print("\nRain attenuation exceeded for %.2lf %% of the time = %.2lf dB\n",p,Arain);
