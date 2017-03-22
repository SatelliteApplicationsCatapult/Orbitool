# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 17:37:52 2015

THIS LIBRARY ACTUALLY IMPORTS PROPA.DLL from CNES
refer to CNES documentation (user manual of library)

***REMOVED***
"""

from sys import path

path.append("../")
import os
import subprocess
import numpy as np
from lbConfiguration import *

# _----------------------------------------------------------------------------------------
def compute_propag(lon, lat, alt, elevation, freq, tilt_polar_angle, diameter, efficiency, availability):
    '''
    This function computes propagation attenuation due to rain conditions, using the CNES library available at :

    description : TODO
    '''

    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = 'applications/linkbudgetweb/arrays/propa_input_array-' + timestr + '.txt'
    np.savetxt(filename,
               np.column_stack((lon, lat, alt, elevation, freq, tilt_polar_angle, diameter, efficiency, availability)))
    cfile = pathtopropa
    Atot = []
    proc = subprocess.Popen([cfile, filename], stdout=subprocess.PIPE)  # runs propa
    (out, err) = proc.communicate()
    for i in range(0, len(out), 9):
        Atot.append(float(out[i:i + 8]))
    Atot = np.asarray(Atot)
    os.remove(filename)

    return Atot
