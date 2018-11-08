"""
script to read in and plot hatsouth light curves
"""
import os
import sys
from PyAstronomy.pyasl import foldAt
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

def plot_full_curve(time, magnitude):
    """
    plot entire dataset for chosen magnitude/aperture
    """
    # plt.plot(time, magnitude)
    plt.scatter(time, magnitude, s=1)
    plt.show()

def phase_fold(dataframe, period, phase=0):
    """
    fold time values, using known period
    """
    time_vals = dataframe.iloc[:, 0]
    mintime = time_vals.min()
    time_vals -= mintime
    print(time_vals)
    folded_time = ((time_vals - phase)/period) % 1 - 0.5
    # short explanation:
    # time values - phase (offset to move the 'dip' to zero)
    # +half period ? some algorithms found online do this idk why ????
    # /period div by period in order to find where in the orbit a point is
    # remainer div % 1, sets every value to be between 0, 1
    # -0.5, simply moves it to -0.5 to 0.5, so centre is at 0


    # print (folded_time)

    # print(phases, epoch)
    print (folded_time)
    return folded_time

if __name__ == '__main__':

    # FOR HATS RAW DATA
    wasp31_raw = load_hats('WASP-31b-HAT-563-0001900.tfalc')
    wasp31 = trim_data(wasp31_raw)

    # FOR WASP RAW DATA
    wasp31_raw = load_wasp('WASP-31_WASP_WASP_a.rdb')
    wasp31 = wasp31_raw

    wasp31_period = 3.405909 # days converted to seconds
    print (wasp31_period)
    wasp31_folded = phase_fold(wasp31, wasp31_period)

    plot_full_curve(wasp31_folded, wasp31.iloc[:, 1])
