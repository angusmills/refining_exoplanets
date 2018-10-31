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

if __name__ == '__main__':

    wasp31 = load_data('WASP-31b-HAT-563-0001900.tfalc')

    trimmed = trim_data(wasp31)
    
    plt.plot(trimmed.iloc[:, 0], trimmed.iloc[:, 1])
    plt.show()