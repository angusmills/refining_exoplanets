"""
Class definitions for star light curves
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# set plotting parameters for publication quality
plt.rcParams['font.size'] = 8
plt.rc('font', family='serif')
plt.rc('xtick', labelsize='5')
plt.rc('ytick', labelsize='5')

def mag_to_flux(mag):
    """
    applies equation for magnitude to flux conversion, then normalizes around 1
    """
    flux = mag.apply(lambda x: 10**(-x/2.5))
    flux /= flux.mean()
    return flux

def bin_by_size(phase, flux, num_of_bins=25):
    """
    splits series into specified num of binned points, w.r.t. 
    """
    binned = []
    dataset = pd.concat([phase, flux], axis=1)
    dataset.columns = ['phase', 'flux']
    length = phase.max()-phase.min()
    bin_time = length/num_of_bins
    lower_bound = phase.min()
    upper_bound = lower_bound + bin_time
    for i in range(num_of_bins):
        points = dataset[(phase > lower_bound) &
                    (phase < upper_bound)]
        avgphase = points['phase'].mean()
        avgflux = points['flux'].mean()
        point = [avgphase, avgflux]
        binned.append(point)
        lower_bound = upper_bound
        upper_bound = lower_bound + bin_time

    binned = pd.DataFrame(binned, columns=['phase', 'flux'])
    return binned

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
        self.wasp['phase'] = (((self.wasp['BJD']+2400000-self.Tc)
                               /self.period+self.phase_offset)
                               %1 - self.phase_offset)
        self.hats['phase'] = (((self.hats['BJD']+2400000-self.Tc)
                               /self.period+self.phase_offset)
                               %1 - self.phase_offset)
        # bin_by_size(self.wasp['phase'], self.wasp['flux'], num_of_bins=500)

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
        plt.figure(figsize=(3, 2.2))
        if source != "hats":
            plt.plot(self.wasp['phase'],
                     self.wasp['flux'],
                     'x',
                     markersize=4,
                     label="SuperWASP",
                     c='black',
                     alpha=0.7,
                     mew=1)
        if source != "wasp":
            plt.plot(self.hats['phase'],
                     self.hats['flux'+str(self.hats_id)],
                     'x',
                     markersize=4,
                     label="HATSouth",
                     c='orange',
                     alpha=0.7,
                     mew=1)
        plt.legend(loc=1)
        plt.xlabel("Phase")
        plt.ylabel("Normalized Flux")
        plt.xticks(np.arange(-0.250, 0.751, 0.125))
        plt.tight_layout(.5)
        plt.savefig("graphs/phase_folded/"+self.name, dpi=300)

    def plot_raw(self, source="both"):
        """
        Graph of raw data for chosen telescope sources
        """
        plt.figure(figsize=(3, 2.2))
        if source != "hats":
            plt.plot(self.wasp['BJD'],
                     self.wasp['flux'],
                     'x',
                     markersize=4,
                     label="SuperWASP",
                     c='black',
                     mew=1)
        if source != "wasp":
            plt.plot(self.hats['BJD'],
                     self.hats['flux'+str(self.hats_id)],
                     'x',
                     markersize=4,
                     label="HATSouth",
                     c='orange',
                     mew=1)
        plt.legend(loc=1)
        plt.xlabel("BJD Time")
        plt.ylabel("Normalized Flux")
        plt.tight_layout(.5)
        plt.savefig("graphs/raw/"+self.name, dpi=300)

    def plot_binned(self, source="both"):
        """
        Graph of phase folded binned data for chosen telescope sources
        """
        plt.figure(figsize=(3, 2.2))
        if source != "hats":
            binned = bin_by_size(self.wasp['phase'], self.wasp['flux'])
            plt.plot(binned['phase'],
                     binned['flux'],
                     'x-',
                     markersize=4,
                     label="SuperWASP",
                     mew=1,
                     linewidth=1,
                     c='black')
        if source != "wasp":
            binned = bin_by_size(self.hats['phase'], self.hats['flux'+str(self.hats_id)])
            plt.plot(binned['phase'],
                     binned['flux'],
                     'x-',
                     markersize=4,
                     label="HATSouth",
                     mew=1,
                     linewidth=1,
                     c='orange')
        plt.legend(loc=4)
        plt.xlabel("Binned Phase")
        plt.ylabel("Normalized Flux")
        plt.tight_layout(.5)
        plt.savefig("graphs/binned/"+self.name, dpi=300)

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

    def to_exofast(self):
        """
        converts file to format correct for exofast online interface
        TODO: attempts to bin the data into <5000 datapoints due to
        limitation of website compute resources
        TODO: combined file
        """
        exo_path = os.path.join(os.getcwd(), 'exofast')
        waspfile = os.path.join(exo_path, self.name+"WASP.txt")
        hatsfile = os.path.join(exo_path, self.name+"HATS.txt")
        with open(waspfile, 'w') as f:
            for i in range(5000):
                f.write('%.5f,%.5f,%.5f' 
                        % (self.wasp['BJD'][i],
                           self.wasp['flux'][i],
                           self.wasp['flux_err'][i]))
                f.write('\n')

# STAR DATA:    NAME      PERIOD     Tc            Duration (hats_id)
WASP_6 = Star("WASP-6", 3.36100208,	2454425.02180, 0.10860)
WASP_31 = Star("WASP-31", 3.4059096, 2455192.6887, 0.1103)
WASP_67 = Star("WASP-67", 4.61442, 2455824.3742, 0.079) #duration in days
WASP_83 = Star("WASP-83", 4.971252, 2455928.8853, 0.1402)
WASP_101 = Star("WASP-101", 3.585720, 2456164.6934, 0.113)

STARS = [WASP_6, WASP_31, WASP_67, WASP_83, WASP_101]
# STARS = [WASP_31]

for star in STARS:
    star.plot_binned(source='both')
