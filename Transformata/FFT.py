import numpy as np


class FFT(object):
    def __init__(self, sampling_frequency, samples_power_of_two):
        """
            samples - 2^samples_power_of_two
            sampling_frequency must be equal to the number of samples
        """
        try:
            self._number_of_samples = 1 << samples_power_of_two
        except ValueError:
            raise ValueError("samples_power_of_two must be an int greater than 0")
        if self._number_of_samples != int(sampling_frequency):
            raise ValueError("sampling_frequency must be equal to the number of samples")
        self._samples_power_of_two = samples_power_of_two
        self._sampling_frequency = int(sampling_frequency)
        self._frequency_bin_resolution = self._sampling_frequency / self._number_of_samples
        self.frequency_bin_x_axis = [self._frequency_bin_resolution * n
                                      for n in range(int(self._sampling_frequency/2))]  # Nyquist limit
        self._W_lookup_table = self._generate_W_lookup_table()
        self._stage0_pair_array = self._generate_pair_array()

    def generate_frequency_bins(self, wave):
        values = []
        for i in range(0, self._number_of_samples, 2):  # values init (stage 0)
            index1 = self._stage0_pair_array[i]
            index2 = self._stage0_pair_array[i+1]
            values += [wave[index1] + wave[index2]]
            values += [wave[index1] - wave[index2]]

        for stage in range(1, self._samples_power_of_two-1, 1):
            temp_values = []
            for row in range(0, self._number_of_samples >> (stage+1), 1):
                stage_row_offset = row * (2 << stage)
                for i in range(1 << stage):
                    a = values[stage_row_offset + i]
                    xa = values[stage_row_offset + (1 << stage) + i]
                    temp_values += [a + self._get_W(i, stage) * xa]
                for i in range(1 << stage):
                    a = values[stage_row_offset + i]
                    xa = values[stage_row_offset + (1 << stage) + i]
                    temp_values += [a - self._get_W(i, stage) * xa]
            values = temp_values

        # we need only half of the results (Nyquist law)
        stage = self._samples_power_of_two-1  # last stage
        temp_values = []
        row = 0
        stage_row_offset = row * (2 << stage)
        for i in range(1 << stage):
            a = values[stage_row_offset + i]
            xa = values[stage_row_offset + (1 << stage) + i]
            temp_values += [a + self._get_W(i, stage) * xa]
        values = temp_values

        #values = np.abs(values)
        return values

    def _get_W(self, power, stage):
        return self._W_lookup_table[stage][power]

    def _generate_W_lookup_table(self):  # generowanie tej listy da się mega przyspieszyć + zmniejszyć wymagane zasoby
        W_array = [
            [
                self._calculate_W(power, index)
                for power in range(index >> 1)
            ] for index in [2 ** x for x in range(1, 10 + 1, 1)]
        ]  # [[W], [W, ...], ...]
        return W_array

    def _calculate_W(self, power, index):
        e_powers = 2 * np.pi * power / index
        return np.cos(e_powers) - np.complex(0, 1) * np.sin(e_powers)

    def _generate_pair_array(self):
        pair_array = []
        for i in range(self._number_of_samples):
            pair_array += [[self._reverse_int(i)]]
        return pair_array  # [[index1, index2], ...]

    def _reverse_int(self, num):
        result = 0
        for i in range(self._samples_power_of_two):
            result = (result << 1) + (num & 1)
            num >>= 1
        return result
