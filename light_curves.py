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
    phase_offset = 0.25
    def __init__(self, name, period, Tc, duration, hats_id=1):
        """
        Reads relevant data, calculates normalized flux (hats only), and
        phase folds time series
        """
        self.name = name
        self.period = period
        self.Tc = Tc
        self.duration = duration
        self.hats_id = 1

        # load datasets
        data_path = os.path.join(os.getcwd(), 'data')
        wasp_path = os.path.join(data_path, 'wasp', (self.name+".rdb"))
        hats_path = os.path.join(data_path, 'hats', (self.name+".tfalc"))

        self.wasp = pd.read_csv(wasp_path,
                                delim_whitespace=True,
                                skiprows=24,
                                names=['BJD', 'flux', 'flux_err', 'filter'])
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
        if bins != None:
            #TODO: create temp arrays where data is binned by phase/bins
            raise NotImplementedError
        if source != "hats":
            plt.scatter(self.wasp['phase'],
                        self.wasp['flux'],
                        s=1,
                        label="WASP")
        if source != "wasp":
            plt.scatter(self.hats['phase'],
                        self.hats['flux'+str(self.hats_id)],
                        s=1,
                        label="HATS")
        plt.legend()
        plt.title("Full dataset of WASP and HATSouth data for "+self.name)
        plt.xlabel("Phase")
        plt.ylabel("Normalized Flux")
        plt.show()

    def std(self):
        """
        Find standard deviations of both datasets
        Ignores data around transit (0.1 width phase centered on Tc)
        """
        wasp_std = (self.wasp[(self.wasp['phase'] > 0.3) |
                    (self.wasp['phase'] < 0.2)]
                    ['flux'].std())
        hats_std = (self.hats[(self.hats['phase'] > 0.3) |
                    (self.hats['phase'] < 0.2)]
                    ['flux'+str(self.hats_id)].std())
        print("For "+self.name+":")
        print("STD of WASP data:", wasp_std, "\nSTD of HATS data:", hats_std)
        return (wasp_std, hats_std)

# STAR DATA:    NAME      PERIOD     Tc            Duration (hats_id)
WASP_6 = Star("WASP-6", 3.36100208,	2454425.02180, 0.10860)
WASP_31 = Star("WASP-31", 3.4059096, 2455192.6887, 0.1103)
WASP_67 = Star("WASP-67", 4.61442, 2455824.3742, 0.079) #duration in days
WASP_83 = Star("WASP-83", 4.971252, 2455928.8853, 0.1402)
WASP_101 = Star("WASP-101", 3.585720, 2456164.6934, 0.113)

STARS = [WASP_6, WASP_31, WASP_67, WASP_83, WASP_101]
# STARS = [WASP_67]

for star in STARS:
    star.std()
