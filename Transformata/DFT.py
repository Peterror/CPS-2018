import numpy as np


class DFT(object):
    def __init__(self, sampling_frequency, number_of_samples, wave):
        self.wave = wave
        self.number_of_samples = number_of_samples
        self.sampling_frequency = sampling_frequency
        self.frequency_bin_resolution = self.sampling_frequency / number_of_samples
        self.frequency_bin_x_axis = [self.frequency_bin_resolution * n
                                     for n in range(int(self.sampling_frequency/2))]  # Nyquist limit

    def generate_frequency_bins(self):
        frequency_bins = []
        N = self.number_of_samples
        n = np.arange(N)

        for k in range(int(self.sampling_frequency/2)):  # Nyquist limit
            e_powers = 2 * np.pi * k * n / N  # it's an array
            Fk_sum = np.sum(self.wave *
                            (np.cos(e_powers) - np.complex(0, 1) * np.sin(e_powers)))  # e^-j*2pi*k*n/N
            frequency_bins += [Fk_sum]
        frequency_bins = (np.abs(frequency_bins)*2)/self.sampling_frequency
        return frequency_bins

    def generate_frequency(self):
        frequency_bins = []
        N = self.number_of_samples
        n = np.arange(N)

        for k in range(int(self.sampling_frequency/2)):  # Nyquist limit
            e_powers = 2 * np.pi * k * n / N  # it's an array
            Fk_sum = [np.sum(self.wave * np.cos(e_powers)) * 2 / self.sampling_frequency,
                      np.sum(self.wave * -np.sin(e_powers)) * 2 / self.sampling_frequency]  # e^-j*2pi*k*n/N
            frequency_bins += [Fk_sum]
        # frequency_bins = (np.abs(frequency_bins)*2)/self.sampling_frequency
        return frequency_bins
