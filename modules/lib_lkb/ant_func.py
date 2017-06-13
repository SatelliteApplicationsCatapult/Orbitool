# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 09:12:39 2014

***REMOVED***


MODULE
"""

import numpy as np
from scipy.special import j1

#_____________________________________________________________________________________________________
######################################################################################################
#         ANTENNA PATTERNS CALCULATIONS
#_____________________________________________________________________________________________________
######################################################################################################


#####################################################################################################
def compute_max_gain(efficiency, ant_diam, freq, flag_calc_type):
    ''' Returns the maximum gain of a parabolic antenna (using theoretical formula) 
        NOTE : Function can take vectors as inputs
        
        Inputs :
            - Scalar or [X] vector of antenna efficiency
            - Scalar or [X] vector of antenna diameter
            - Scalar or [X] vector of antenna frequency
            - Scalar or [X] vector of flag_calc_type : 'parab_theo' or 'gauss_beam' 
            (note that for this last parameter, actually the same calculation is performed)
        
    '''
    
    if flag_calc_type[0] == 'parab_theo': 
        return 10*np.log10(efficiency * (np.pi * ant_diam)**2 / (3e8 / (freq * 1e6))**2)
    elif flag_calc_type[0] == 'gauss_beam': 
        # source : Balanis book (conical horns)
#        optimal_length      = ant_diam ** 2 / ( 3 * (3e8/(freq * 1e6)))
#        max_phase_dev = ant_diam **2 / (8 * (3e8/(freq * 1e6)) * )
#        loss_figure         = 0.8 - 1.71*max_phase_dev + 26.25 * max_phase_dev**2 -17.79 * max_phase_dev**3
        return 10*np.log10(efficiency * (np.pi * ant_diam)**2 / (3e8 / (freq * 1e6))**2)
#####################################################################################################




####################################################################################################
def compute_sat_ant_gain(az_elev, ant_diam, freq, max_gain, flag_calc_type, theta_3dB):
    '''
    This is just a wrapper that allows to input az-elev arguments for computing antenna gain in a given direction
    '''
# TODO : ERROR DB AND NO DB
    values = 0
    # compute angle to beam center (since radiation pattern is symmetrical)
    angles_beam = az_elev[1,:] # only elevation is used : assumption that radiation pattern is symmetric
    
    #TODO : check flag calc_type more rigorously (not only take first value)
    if flag_calc_type[0] == 'parab_theo': 

        values = calc_pattern_beam(angles_beam, ant_diam, freq, flag_calc_type[0])    
        values = max_gain + 10*np.log10(values)
        
    elif flag_calc_type[0] == 'gauss_beam':
        
        #TODO : change flag_calc_type[0] in below
        values = calc_pattern_beam(angles_beam, ant_diam, freq, flag_calc_type[0], theta_3dB = theta_3dB * np.pi/180)
        values = max_gain + 10*np.log10(values)
        
    elif flag_calc_type[0] == 'ITU_S1428.1':
        #WARNING : in values in degrees, out values already in dB
        pass        
        
        
        
            
    return values

####################################################################################################



#####################################################################################################   
def calc_pattern_beam(theta, diam, freq, flag_calc_type, theta_3dB = np.nan):
    '''
    This function calculates the radiation pattern of a gaussian illuminated beam
    (Formula found on the Internet but verified) ==> has been cross checked
    Input theta : 1D vectors of angles where to compute the perfo (no need for az/elev since symmetry)
    Input diam : antenna diameter
    Input freq : frequency
    NOTE : diam and feq could also be 1D vectors of same size as theta : in that case the function computes the performance for each triplet
    '''
    
    if flag_calc_type == 'parab_theo':
        theta[np.abs(theta) <= 1e-10] = 1e-10
        wavelength = 3e8/(freq*1e6)
        return (2 * j1(np.sin(theta)*np.pi*diam / wavelength) / (np.sin(theta) * np.pi * diam / wavelength ))**2 
        
    elif flag_calc_type == 'gauss_beam':
        theta[np.abs(theta) <= 1e-10] = 1e-10
        a =  -3  / (theta_3dB)**2 # WARNING : This is considering theta3dB as a SEMI-ANGLE and not the FULL angle (like in the 70 lambda/ D formula)
        return 10**((a * (theta)**2)/10)
        
    elif flag_calc_type == 'ITU_S1428.1':
        
        result = np.empty_like(theta)
        Gmax = np.empty_like(theta)
        wavelength = 3e8/(freq*1e6)
        diam = np.atleast_1d(diam)
        wavelength = np.atleast_1d(wavelength)
        theta = np.atleast_1d(theta)
        
        if np.size(diam) == 1:
            diam = np.repeat(diam, np.size(theta), axis = 0)
            
        if np.size(wavelength) == 1:
            wavelength = np.repeat(wavelength, np.size(theta), axis = 0)
        
        rap_diam_wavelength = diam/wavelength + 1e-8
        

        
        # Case lambda / D between 20 and 25
        mask_20_25 = np.logical_and(rap_diam_wavelength < 25, rap_diam_wavelength >= 20)
        result[mask_20_25], Gmax[mask_20_25] = apply_itu_pattern_1428(diam[mask_20_25], wavelength[mask_20_25], theta[mask_20_25], '>20<25')
        
        # Case lambda / D between 25 and 100
        mask_25_100 = np.logical_and(rap_diam_wavelength < 100, rap_diam_wavelength > 25)
        result[mask_25_100], Gmax[mask_25_100] = apply_itu_pattern_1428(diam[mask_25_100], wavelength[mask_25_100], theta[mask_25_100], '>25<100')
        
        # Case lambda / D over 100
        mask_sup_100 = rap_diam_wavelength >= 100
        result[mask_sup_100], Gmax[mask_sup_100] = apply_itu_pattern_1428(diam[mask_sup_100], wavelength[mask_sup_100], theta[mask_sup_100], '>100')
        
        # Other cases  (e.g. lesser than 20)
        mask_else = np.logical_not(np.logical_or(mask_20_25, mask_25_100, mask_sup_100))
        result[mask_else] = np.nan
        Gmax[mask_else] = np.nan

        return result, Gmax
        
        
####################################################################################################    

####################################################################################################
def apply_itu_pattern_1428(diam, wavelength, phi, flag_pattern):
    '''
    Apply ITU pattern adequately to ITU regulation S1428.1 (from RR2012) :
    "Reference FSS earth-station radiation patterns for use in interference assessment involving non-GSO satellites in frequency bands between 10.7 GHz and 30 GHz"
    '''
    phi = np.abs(phi)
    res = np.empty_like(phi)    
    
    if flag_pattern == '>20<25':
        
        Gmax                                                                            =   20 * np.log10(diam/wavelength) + 7.7
        G1                                                                              =   29 - 25 * np.log10(95 * wavelength / diam)
        phi_m                                                                           =   20 * (wavelength / diam) * np.sqrt(Gmax - G1)
        
        res[phi < phi_m]                                                                =   Gmax[phi < phi_m] - 2.5 * 1e-3 * (diam[phi < phi_m] / wavelength[phi < phi_m] * phi[phi < phi_m])**2
        res[np.logical_and(phi >= phi_m                , phi< 95* wavelength / diam)]   =   G1[np.logical_and(phi >= phi_m , phi< 95* wavelength / diam)] 
        res[np.logical_and(phi >= 95* wavelength / diam, phi < 33.1)]                   =   29 - 25 * np.log10(phi[np.logical_and(phi>= 95* wavelength / diam, phi < 33.1)])
        res[np.logical_and(phi >= 33.1                 , phi < 80)]                     =   -9
        res[np.logical_and(phi >= 80                   , phi < 180)]                    =   -5
    
    if flag_pattern == '>25<100':

        Gmax                                                                            =   20 * np.log10(diam/wavelength) + 7.7
        G1                                                                              =   29 - 25 * np.log10(95 * wavelength / diam)
        phi_m                                                                           =   20 * (wavelength / diam) * np.sqrt(Gmax - G1)
       
        res[phi < phi_m]                                                                =   Gmax[phi < phi_m] - 2.5 * 1e-3 * (diam[phi < phi_m] / wavelength[phi < phi_m] * phi[phi < phi_m])**2
        res[np.logical_and(phi >= phi_m                , phi< 95* wavelength / diam)]   =   G1[np.logical_and(phi >= phi_m, phi< 95* wavelength / diam)]
        res[np.logical_and(phi >= 95* wavelength / diam, phi < 33.1)]                   =   29 - 25 * np.log10(phi[np.logical_and(phi>= 95* wavelength / diam, phi < 33.1)])
        res[np.logical_and(phi >= 33.1                 , phi < 80)]                     =   -9
        res[np.logical_and(phi >= 80                   , phi < 120)]                    =   -4
        res[np.logical_and(phi >= 120                  , phi < 180)]                    =   -9
        
    if flag_pattern == '>100':
            
        Gmax                                                                            =   20 * np.log10(diam/wavelength) + 8.4
        G1                                                                              =   -1 - 15 * np.log10(wavelength / diam)
        phi_m                                                                           =   20 * (wavelength / diam) * np.sqrt(Gmax - G1)
        phi_r                                                                           =   15.85 * (diam / wavelength)**-0.6
        
        res[phi < phi_m]                                                                =   Gmax[phi < phi_m] - 2.5 * 1e-3 * (diam[phi < phi_m] / wavelength[phi < phi_m] * phi[phi < phi_m])**2
        res[np.logical_and(phi >= phi_m                , phi<phi_r)]                    =   G1[np.logical_and(phi >= phi_m, phi<phi_r)]
        res[np.logical_and(phi >= phi_r                , phi<10)]                       =   29 - 25 * np.log10(phi[np.logical_and(phi>=phi_r, phi<10)])
        res[np.logical_and(phi >= 10                   , phi<34.1)]                     =   34 - 30 * np.log10(phi[np.logical_and(phi>=10, phi<34.1)])
        res[np.logical_and(phi >= 34.1                 , phi < 80)]                     =   -12
        res[np.logical_and(phi >= 80                   , phi < 120)]                    =   -7
        res[np.logical_and(phi >= 120                  , phi < 180)]                    =   -12
        
    return res, Gmax
####################################################################################################
