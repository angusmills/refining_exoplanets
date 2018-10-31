"""
script to read in and plot hatsouth light curves
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_data(filename):
    """
    load full file of chosen dataset into pandas dataframe
    """
    filepath = os.path.join(os.getcwd(), 'data', filename)
    input_data = pd.read_csv(filepath, delim_whitespace=True, skiprows=[0])
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
    plot full  
    """
    plt.plot(time, magnitude)
    plt.scatter(time, magnitude, s=5)
    plt.show()

if __name__ == '__main__':

    wasp31_raw = load_data('WASP-31b-HAT-563-0001900.tfalc')

    wasp31 = trim_data(wasp31_raw)

    plot_full_curve(wasp31.iloc[:,0], wasp31.iloc[:, 1])