import numpy as np


# Klasy bazowe

class SygnalCiagly(object):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania):
        self.A = amplituda
        if czas_poczatkowy > 0:
            self.t1 = czas_poczatkowy
        else:
            self.t1 = 0
        self.d = czas_trwania
        self.f_p = f_probkowania
        self._czas_trwania_czystego_sygnalu = self.d - self.t1
        self._ilosc_probek_wlasciwych = int(self._czas_trwania_czystego_sygnalu / self.f_p)
        self.T = okres

    def generuj(self):
        """
        :return: ndarray of samples
        """
        raise NotImplementedError

    def srednia(self):
        return np.sum(self.x*self.f_p)/len(self.x)

    def srednia_bezwzgledna(self):
        return np.sum(np.abs(self.x*self.f_p)) / len(self.x)

    def moc_srednia(self):
        return np.sum((self.x**2)*self.f_p) / len(self.x)

    def wariancja_wokol_sredniej(self):
        return np.sum(((self.x-self.srednia)**2)*self.f_p) / len(self.x)

    def wartosc_skuteczna(self):
        return np.sqrt(self.moc_srednia())


# Klasy dziedziczace

class SzumORozkladzieJednostajnym(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania):
        super(SzumORozkladzieJednostajnym, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)

    def generuj(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p)).fill(0)
        return np.append(poczatkowe_zera, 2 * self.A * np.random.ranf(self._ilosc_probek_wlasciwych) - self.A)


class SzumGaussowski(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania):
        super(SzumGaussowski, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)

    def generuj(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p)).fill(0)
        return np.append(poczatkowe_zera, np.random.randn(self._ilosc_probek_wlasciwych))


class Sinusoida(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania):
        super(Sinusoida, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)

    def generuj(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p)).fill(0)
        t = np.arange(0, self._czas_trwania_czystego_sygnalu + self.f_p, self.f_p)
        return np.append(poczatkowe_zera, self.A * np.sin(t))


class SinusoidaWyprostowanaJednopolowkowo(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania):
        super(SinusoidaWyprostowanaJednopolowkowo, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)

    def generuj(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p)).fill(0)
        t = np.arange(0, self._czas_trwania_czystego_sygnalu + self.f_p, self.f_p)
        x_sin = np.sin(t)
        return np.append(poczatkowe_zera, 0.5 * self.A * (x_sin + np.abs(x_sin)))


class SinusoidaWyprostowanaDwupolowkowo(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania):
        super(SinusoidaWyprostowanaDwupolowkowo, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)

    def generuj(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p)).fill(0)
        t = np.arange(0, self._czas_trwania_czystego_sygnalu + self.f_p, self.f_p)
        return np.append(poczatkowe_zera, np.abs(np.sin(t)))


class Prostokat(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania, wspolczynnik_wypelnienia):
        super(Prostokat, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)
        self.k_w = wspolczynnik_wypelnienia

    def generuj(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p)).fill(0)
        x = np.empty(self._ilosc_probek_wlasciwych)
        for i in range(self._ilosc_probek_wlasciwych):
            t = self.f_p * i
            k = int((i * self.f_p)/self.T)
            if (k*self.T + self.t1) <= t < (self.k_w*self.T + k*self.T + self.t1):
                x[i] = 1
            else:
                x[i] = 0
        return np.append(poczatkowe_zera, x)


class ProstokatSymetryczny(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania):
        super(ProstokatSymetryczny, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)

    def generuj(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p)).fill(0)
        return np.append(poczatkowe_zera)
        raise NotImplementedError()


class Trojkat(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania):
        super(Trojkat, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)

    def generuj(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p)).fill(0)
        return np.append(poczatkowe_zera)
        raise NotImplementedError()


class SkokJednostkowy(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania, t_skoku):
        super(SkokJednostkowy, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)
        self.t_s = t_skoku

    def generuj(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p)+int((self.t_s-self.t1)/self.f_p)).fill(0)
        poczatkowe_zera[-1] = self.A/2
        koncowe_zera = np.empty(int(self.d-self.t_s)).fill(self.A)
        return np.append(poczatkowe_zera, koncowe_zera)
