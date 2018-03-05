import numpy as np


# Klasy bazowe

class SygnalDyskretny(object):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, f_probkowania):
        self.A = amplituda
        if czas_poczatkowy > 0:
            self.t1 = czas_poczatkowy
        else:
            self.t1 = 0
        self.d = czas_trwania
        self.f_p = f_probkowania
        self.ilosc_probek = int(self.d/self.f_p)
        self.x = self.generuj()

    def generuj(self):
        """
        :return: ndarray of samples
        """
        raise NotImplementedError

    def srednia(self):
        return np.sum(self.x)/len(self.x)

    def srednia_bezwzgledna(self):
        return np.sum(np.abs(self.x)) / len(self.x)

    def moc_srednia(self):
        return np.sum(self.x**2) / len(self.x)

    def wariancja_wokol_sredniej(self):
        return np.sum((self.x-self.srednia)**2) / len(self.x)

    def wartosc_skuteczna(self):
        return np.sqrt(self.moc_srednia())


# Klasy dziedziczace

class ImpulsJednostkowy(SygnalDyskretny):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania,  f_probkowania):
        super(ImpulsJednostkowy, self).__init__(amplituda, czas_poczatkowy, czas_trwania,  f_probkowania)

    def generuj(self):
        raise NotImplementedError()


class SzumImpulsowy(SygnalDyskretny):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania,  f_probkowania):
        super(SzumImpulsowy, self).__init__(amplituda, czas_poczatkowy, czas_trwania,  f_probkowania)

    def generuj(self):
        raise NotImplementedError()
