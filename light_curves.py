"""
Class definitions for star light curves
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

def mag_to_flux(mag):
    """
    applies equation for magnitude to flux conversion, then normalizes around 1
    """
    flux = mag.apply(lambda x: 10**(-x/2.5))
    flux /= flux.mean()
    return flux

class Star():
    """
    A set of data for one star
    support for both HATSouth and WASP light curves
    """
    def __init__(self, name, period, Tc, duration):
        """
        Reads relevant data, calculates normalized flux (hats only), and
        phase folds time series
        """
        self.name = name
        self.hats_id = 1
        self.period = period
        self.Tc = Tc
        self.duration = duration
        self.phase_offset = 0.25

        # load datasets
        data_path = os.path.join(os.getcwd(), 'data')
        hats_path = os.path.join(data_path, 'hats', (self.name+".tfalc"))
        wasp_path = os.path.join(data_path, 'wasp', (self.name+".rdb"))

        self.hats = pd.read_csv(hats_path,
                                delim_whitespace=True,
                                skiprows=1,
                                header=None,
                                usecols=[3, 19, 20, 21, 5, 8, 11, 6, 9, 12],
                                names=['BJD',
                                       'err1', 'qual1',
                                       'err2', 'qual2',
                                       'err3', 'qual3',
                                       'mag1', 'mag2', 'mag3'])
        self.wasp = pd.read_csv(wasp_path,
                                delim_whitespace=True,
                                skiprows=24,
                                names=['BJD', 'flux', 'flux_err', 'filter'])

        # Calculate normalized flux, for equal comparisons between HATS/WASP
        for i in [1, 2, 3]:
            self.hats['flux'+str(i)] = mag_to_flux(self.hats['mag'+str(i)])

        # Phase folding, according to given phase, Tc
        self.wasp['phase'] = ((self.wasp['BJD']+2400000-self.Tc)
                              /self.period+self.phase_offset) % 1
        self.hats['phase'] = ((self.hats['BJD']+2400000-self.Tc)
                              /self.period+self.phase_offset) % 1

    def plot(self, source="both", bins=None):
        """
        Graph of phase folded data for chosen telescope sources
        """
        # OLD BIN CODE: not functional currently
        # if bins != None:
        #     samples = len(magnitude)
        #     iterations = len(range(samples))//bins
        #     time = time.rolling(bins).mean()
        #     magnitude = magnitude.rolling(bins).mean()
        # BINS NEEDS REFACTORING TO BE TIME DEPENDENT...
        if source != "hats":
            plt.scatter(self.wasp['phase'],
                        self.wasp['flux'],
                        s=1)
        if source != "wasp":
            plt.scatter(self.hats['phase'],
                        self.hats['flux'+str(self.hats_id)],
                        s=1)
        plt.show()

WASP_31 = Star("WASP-31", 3.4059096, 2455192.6887, 0)
WASP_31.plot()
