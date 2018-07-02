import numpy as np
import copy
import random
import math

# Klasy bazowe

class SygnalDyskretny(object):
    def __init__(self, amplituda, numer_pierwszej_probki, czas_trwania, f_probkowania):
        self.A = amplituda
        self.d = czas_trwania
        self.n1 = numer_pierwszej_probki
        self.f_p = f_probkowania
        self.ilosc_probek = int(self.d/self.f_p) + 1
        self.y = None  # inicjalizowane w klasach potomnych
        self.x = np.arange(self.ilosc_probek) * f_probkowania

    def __add__(self, other):
        if self.y.size == other.y.size:
            sygnal_wynikowy = copy.deepcopy(self)
            sygnal_wynikowy.y = self.y + other.y
        elif self.y.size < other.y.size:
            sygnal_wynikowy = copy.deepcopy(other)
            zera = np.empty(other.y.size - self.y.size)
            zera.fill(0)
            sygnal_wynikowy.y = np.append(self.y, zera) + other.y
        else:
            sygnal_wynikowy = copy.deepcopy(self)
            zera = np.empty(self.y.size - other.y.size)
            zera.fill(0)
            sygnal_wynikowy.y = self.y + np.append(other.y, zera)
        return sygnal_wynikowy

    def __sub__(self, other):
        if self.y.size == other.y.size:
            sygnal_wynikowy = copy.deepcopy(self)
            sygnal_wynikowy.y = self.y - other.y
        elif self.y.size < other.y.size:
            sygnal_wynikowy = copy.deepcopy(other)
            zera = np.empty(other.y.size - self.y.size)
            zera.fill(0)
            sygnal_wynikowy.y = np.append(self.y, zera) - other.y
        else:
            sygnal_wynikowy = copy.deepcopy(self)
            zera = np.empty(self.y.size - other.y.size)
            zera.fill(0)
            sygnal_wynikowy.y = self.y - np.append(other.y, zera)
        return sygnal_wynikowy

    def __mul__(self, other):
        if self.y.size == other.y.size:
            sygnal_wynikowy = copy.deepcopy(self)
            sygnal_wynikowy.y = self.y * other.y
        elif self.y.size < other.y.size:
            sygnal_wynikowy = copy.deepcopy(other)
            zera = np.empty(other.y.size - self.y.size)
            zera.fill(0)
            sygnal_wynikowy.y = np.append(self.y, zera) * other.y
        else:
            sygnal_wynikowy = copy.deepcopy(self)
            zera = np.empty(self.y.size - other.y.size)
            zera.fill(0)
            sygnal_wynikowy.y = self.y * np.append(other.y, zera)
        return sygnal_wynikowy

    def __truediv__(self, other):
        if self.y.size == other.y.size:
            sygnal_wynikowy = copy.deepcopy(self)
            sygnal_wynikowy.y = self.y / other.y
        elif self.y.size < other.y.size:
            sygnal_wynikowy = copy.deepcopy(other)
            zera = np.empty(other.y.size - self.y.size)
            zera.fill(0)
            sygnal_wynikowy.y = np.append(self.y, zera) / other.y
        else:
            sygnal_wynikowy = copy.deepcopy(self)
            zera = np.empty(self.y.size - other.y.size)
            zera.fill(0)
            sygnal_wynikowy.y = self.y / np.append(other.y, zera)
        return sygnal_wynikowy

    def _generuj_probki(self):
        """
        :return: ndarray of samples
        """
        raise NotImplementedError

    def generuj_uklad_xy(self):
        """
        :return: tuple(x(t), t)
        """
        return self.x, self.y

    def srednia(self):
        return np.sum(self.y)/len(self.y)

    def srednia_bezwzgledna(self):
        return np.sum(np.abs(self.y)) / len(self.y)

    def moc_srednia(self):
        return np.sum(self.y**2) / len(self.y)

    def wariancja_wokol_sredniej(self):
        return np.sum((self.y-self.srednia())**2) / len(self.y)

    def wartosc_skuteczna(self):
        return np.sqrt(self.moc_srednia())

    def splot(self, sygnal_b, M=None):
        ilosc_probek = self.y.size + sygnal_b.y.size - 1

        y = [0 for i in range(ilosc_probek)]
        x = np.arange(0, ilosc_probek)
        if M is None:
            for n in range(ilosc_probek):
                for k in range(0, self.y.size):
                    if (n-k) < 0:
                        break
                    try:
                        # h(k) * x(n-k)
                        temp = self.y[k] * sygnal_b.y[n-k]
                        y[n] += temp
                        pass
                    except IndexError:
                        pass
        else:
            for n in range(ilosc_probek):
                for k in range(0, M):
                    if (n-k) < 0:
                        break
                    try:
                        # h(k) * x(n-k)
                        temp = self.y[k] * sygnal_b.y[n-k]
                        y[n] += temp
                        pass
                    except IndexError:
                        pass
        y = np.array(y)
        return SygnalDyskretnyNieokreslony(x=x, y=y)
# Klasy dziedziczace


class SygnalDyskretnyNieokreslony(SygnalDyskretny):
    def __init__(self, x, y):
        super(SygnalDyskretnyNieokreslony, self).__init__(np.max(y), 0, np.max(x), 1)
        self.x = x
        self.y = y

    def _generuj_probki(self):
        pass

class ImpulsJednostkowy(SygnalDyskretny):
    def __init__(self, amplituda, numer_pierwszej_probki, czas_trwania, f_probkowania, numer_probki_skoku):
        super(ImpulsJednostkowy, self).__init__(amplituda, numer_pierwszej_probki, czas_trwania,  f_probkowania)
        self.numer_probki_skoku = numer_probki_skoku
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        poczatkowe_zera = np.empty(int(self.ilosc_probek))
        poczatkowe_zera.fill(0)
        poczatkowe_zera[self.numer_probki_skoku + self.n1] = self.A
        return poczatkowe_zera


class SzumImpulsowy(SygnalDyskretny):
    def __init__(self, amplituda, numer_pierwszej_probki, czas_trwania, f_probkowania, prawdopodobienstwo):
        super(SzumImpulsowy, self).__init__(amplituda, numer_pierwszej_probki, czas_trwania,  f_probkowania)
        self.p = prawdopodobienstwo
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        poczatkowe_zera = np.empty(int(self.ilosc_probek))
        poczatkowe_zera.fill(0)
        for i in range(poczatkowe_zera.size):
            if (self.n1 < i) and (self.p > random.random()):
                poczatkowe_zera[i] = self.A
        return poczatkowe_zera


class OknoHamminga(SygnalDyskretny):
    def __init__(self, M):
        super(OknoHamminga, self).__init__(amplituda=1.0, numer_pierwszej_probki=0, czas_trwania=M, f_probkowania=1)
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        poczatkowe_zera = np.empty(int(self.ilosc_probek))
        poczatkowe_zera.fill(0)
        for i in range(poczatkowe_zera.size):
            poczatkowe_zera[i] = 0.53836 - 0.46164 * math.cos(2 * math.pi * i / self.ilosc_probek)
        return poczatkowe_zera


class OknoHanninga(SygnalDyskretny):
    def __init__(self, M):
        super(OknoHanninga, self).__init__(amplituda=1.0, numer_pierwszej_probki=0, czas_trwania=M, f_probkowania=1)
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        poczatkowe_zera = np.empty(int(self.ilosc_probek))
        poczatkowe_zera.fill(0)
        for i in range(poczatkowe_zera.size):
            poczatkowe_zera[i] = 0.5 - 0.5 * math.cos(2 * math.pi * i / self.ilosc_probek)
        return poczatkowe_zera


class OknoBlackmana(SygnalDyskretny):
    def __init__(self, M):
        super(OknoBlackmana, self).__init__(amplituda=1.0, numer_pierwszej_probki=0, czas_trwania=M, f_probkowania=1)
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        poczatkowe_zera = np.empty(int(self.ilosc_probek))
        poczatkowe_zera.fill(0)
        for i in range(poczatkowe_zera.size):
            poczatkowe_zera[i] = 0.42 - 0.5 * math.cos(2 * math.pi * i / self.ilosc_probek) \
                                 + 0.08 * math.cos(4 * math.pi * i / self.ilosc_probek)
        return poczatkowe_zera
