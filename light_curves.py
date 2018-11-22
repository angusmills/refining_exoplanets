"""
script to read in and plot hatsouth light curves
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_hats(filename):
    """
    load full file of chosen HATSouth dataset into df
    """
    filepath = os.path.join(os.getcwd(), 'data', filename)
    input_data = pd.read_csv(filepath, delim_whitespace=True, skiprows=[0])
    return input_data

def load_wasp(filename):
    """
    load full file of chosen WASP dataset into df
    """
    filepath = os.path.join(os.getcwd(), 'data', filename)
    input_data = pd.read_csv(filepath, delim_whitespace=True, skiprows=25)
    return input_data

def trim_data(dataframe):
    """
    datafiles have huge amount of data
    trim dataframe to only have relevant data
    """
    trimmed = dataframe.iloc[:, [3, 19, 20, 21, 5, 8, 11, 6, 9, 12]]
    trimmed.columns = ['BJD',
                       'mag1', 'mag2', 'mag3',
                       'err1', 'err2', 'err3',
                       'qual1', 'qual2', 'qual3']
    return trimmed

def plot_curve(time, magnitude, binned=0, n=5):
    """
    plot entire dataset for chosen magnitude/aperture
    """
    if binned == 1:
        samples = len(magnitude)
        iterations = len(range(samples))//n
        time = time.rolling(n).mean()
        magnitude = magnitude.rolling(n).mean()

    plt.scatter(time, magnitude, s=1)
    plt.show()

def phase_fold(time, period, phase=0):
    """
    fold time values, using known period
    """
    time -= time.min()
    folded_time = ((time-phase)/period) % 1 - 0.5
    # short explanation:
    # time values - phase (offset to move the 'dip' to zero) phase in days
    # /period div by period in order to find where in the orbit a point is
    # remainer div % 1, sets every value to be between 0, 1
    # -0.5, simply moves it to -0.5 to 0.5, so centre is at 0
    return folded_time

def mag_to_flux(mag):
    flux = 10**(-mag/2.5)
    return flux

def to_normalized_flux(magnitude):
    """
    WASP and HATS have 'brightness' measures in different units
    function changes magnitude to normalized flux, to compare both curves
    """
    flux = magnitude.apply(mag_to_flux)
    avg = flux.mean()
    flux /= avg
    return flux

def main_func(HATSname, WASPname, period, HATSphase, WASPphase):

    # FOR HATS RAW DATA
    hats_wasp_raw = load_hats(HATSname)
    hats_wasp = trim_data(hats_wasp_raw)

    # FOR WASP RAW DATA
    wasp_wasp_raw = load_wasp(WASPname)
    wasp_wasp = wasp_wasp_raw

    wasp_period = period # period, in days
    hats_wasp_folded = phase_fold(hats_wasp.iloc[:, 0], wasp_period, phase=HATSphase)
    wasp_wasp_folded = phase_fold(wasp_wasp.iloc[:, 0], wasp_period, phase=WASPphase)

    hats_wasp.loc[:, 'mag1'] = to_normalized_flux(hats_wasp['mag1'])

    plt.scatter(wasp_wasp_folded, wasp_wasp.iloc[:, 1], s=5)
    plt.scatter(hats_wasp_folded, hats_wasp.iloc[:, 1], s=5)
    plt.show()

    plot_curve(hats_wasp_folded, hats_wasp.iloc[:, 1], binned=0)
    plot_curve(wasp_wasp_folded, wasp_wasp.iloc[:, 1], binned=0)

# TODO: find Tc, or method to use found mid-points
#       plot both on one axis DONE
#       find method to centre phase folded times to zero
#       'score' each period change to find optimal refined period
#       plot error bars
#       fix dataframe warning message
#       order times+flux according to times