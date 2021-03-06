import numpy as np
import copy
from Generator.SygnalDyskretny import SygnalDyskretny, SygnalDyskretnyNieokreslony


# Klasy bazowe

class SygnalCiagly(object):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania=0.01):
        self.A = amplituda
        if czas_poczatkowy > 0:
            self.t1 = czas_poczatkowy
        else:
            self.t1 = 0
        self.d = czas_trwania
        self.f_p = f_probkowania
        self._czas_trwania_czystego_sygnalu = self.d - self.t1
        self._ilosc_probek_wlasciwych = int(self._czas_trwania_czystego_sygnalu / self.f_p) + 1
        self.T = okres
        self.y = None  # inicjalizowane w klasach potomnych
        self.x = np.arange(self._ilosc_probek_wlasciwych) * f_probkowania
        self.T_kwantyzacji = None
        self.n_kwantyzacji = None
        self.kwantyzacja_y = None
        self.kwantyzacja_x = None
        self.ekstrapolacja0_y = None
        self.ekstrapolacja1_y = None

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
        Inicjalizuje self.x ndarray próbek
        """
        raise NotImplementedError

    def generuj_uklad_xy(self):
        """
        :return: tuple(x(t), t)
        """
        return self.x, self.y

    def srednia(self):
        return np.sum(self.y*self.f_p)/self.y.size

    def srednia_bezwzgledna(self):
        return np.sum(np.abs(self.y*self.f_p)) / self.y.size

    def moc_srednia(self):
        return np.sum((self.y**2)*self.f_p) / self.y.size

    def wariancja_wokol_sredniej(self):
        return np.sum(((self.y-self.srednia())**2)*self.f_p) / self.y.size

    def wartosc_skuteczna(self):
        return np.sqrt(self.moc_srednia())

    def kwantyzacja_z_obcieciem(self, T_kwantyzacji, n_kwantyzacji):
        self.T_kwantyzacji = T_kwantyzacji
        self.n_kwantyzacji = n_kwantyzacji
        podzialka = self.A / n_kwantyzacji * 2

        def _kwantyzuj(v):
            return podzialka * int((v+self.A)/podzialka) - self.A

        x_step = int(self.T_kwantyzacji/self.f_p)
        hor_podzialka = int(self.y.size/x_step)
        y = np.arange(0, hor_podzialka, 1)
        for j in range(hor_podzialka):
                y[j] = _kwantyzuj(np.min(self.y[j * x_step: j * x_step + x_step]))
        self.kwantyzacja_y = y
        self.kwantyzacja_x = np.arange(0, hor_podzialka, 1) * self.T_kwantyzacji
        return self

    def kwantyzacja_z_zaokragleniem(self, T_kwantyzacji, n_kwantyzacji):
        self.T_kwantyzacji = T_kwantyzacji
        self.n_kwantyzacji = n_kwantyzacji
        podzialka = self.A / n_kwantyzacji * 2

        def _kwantyzuj(v):
            return podzialka * int((v+self.A)/podzialka) - self.A

        x_step = int(self.T_kwantyzacji/self.f_p)
        hor_podzialka = int(self.y.size/x_step)
        y = np.arange(0, hor_podzialka, 1)
        for j in range(hor_podzialka):
                y[j] = _kwantyzuj(np.average(self.y[j * x_step: j * x_step + x_step]))
        self.kwantyzacja_y = y
        self.kwantyzacja_x = np.arange(0, hor_podzialka, 1) * self.T_kwantyzacji
        return self

    def ekstrapolacja_0rzedu(self):
        podzialka = self.A / self.n_kwantyzacji * 2
        x_step = int(self.T_kwantyzacji/self.f_p)

        temp_y = np.empty(self.y.size)
        temp_y.fill(0)
        for i in range(self.kwantyzacja_x.size):
            for j in range(x_step):
                temp_y[i*x_step + j] = self.kwantyzacja_y[i]

        self.ekstrapolacja0_y = temp_y
        return temp_y

    def ekstrapolacja_1rzedu(self):
        podzialka = self.A / self.n_kwantyzacji * 2
        x_step = int(self.T_kwantyzacji/self.f_p)

        temp_y = np.empty(self.y.size)
        temp_y.fill(0)
        for i in range(self.kwantyzacja_x.size-1):
            y_step = (self.kwantyzacja_y[i+1] - self.kwantyzacja_y[i]) / x_step
            for j in range(x_step):
                temp_y[i * x_step + j] = y_step*j + self.kwantyzacja_y[i]

        self.ekstrapolacja1_y = temp_y
        return temp_y

    def sinc(self):
        raise NotImplementedError

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

    def korelacja(self, sygnal_b, M=None):
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
                        temp = self.y[k] * sygnal_b.y[-1-(n-k)]  # dostęp do elementów od końca
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
                        temp = self.y[k] * sygnal_b.y[-1-(n-k)]
                        y[n] += temp
                        pass
                    except IndexError:
                        pass
        y = np.array(y)
        return SygnalDyskretnyNieokreslony(x=x, y=y)

# Klasy dziedziczace

class SygnalCiaglyNieokreslony(SygnalCiagly):
    def __init__(self, x, y, T_kwantyzacji=None, n_kwantyzacji=None):
        super(SygnalCiaglyNieokreslony, self).\
            __init__(None, 0, x[-1], None, x[1] - x[0])
        self.x = copy.copy(x)
        self.y = copy.copy(y)
        self.T_kwantyzacji = T_kwantyzacji
        self.n_kwantyzacji = n_kwantyzacji

    def _generuj_probki(self):
        return None

    def srednia(self):
        return None

    def srednia_bezwzgledna(self):
        return None

    def moc_srednia(self):
        return None

    def wariancja_wokol_sredniej(self):
        return None

    def wartosc_skuteczna(self):
        return None


class SzumORozkladzieJednostajnym(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania):
        super(SzumORozkladzieJednostajnym, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p))
        poczatkowe_zera.fill(0)
        return np.append(poczatkowe_zera, 2 * self.A * np.random.ranf(self._ilosc_probek_wlasciwych) - self.A)


class SzumGaussowski(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania):
        super(SzumGaussowski, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p))
        poczatkowe_zera.fill(0)
        return np.append(poczatkowe_zera, np.random.randn(self._ilosc_probek_wlasciwych) * self.A)


class Sinusoida(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania):
        super(Sinusoida, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p))
        poczatkowe_zera.fill(0)
        t = np.arange(0, self._ilosc_probek_wlasciwych) * self.f_p
        return np.append(poczatkowe_zera, self.A * np.sin(2*np.pi/self.T * (t-self.t1)))


class SinusoidaWyprostowanaJednopolowkowo(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania):
        super(SinusoidaWyprostowanaJednopolowkowo, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p))
        poczatkowe_zera.fill(0)
        t = np.arange(0, self._czas_trwania_czystego_sygnalu + self.f_p, self.f_p)
        x_sin = np.sin(2*np.pi/self.T * (t-self.t1))
        return np.append(poczatkowe_zera, 0.5 * self.A * (x_sin + np.abs(x_sin)))


class SinusoidaWyprostowanaDwupolowkowo(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania):
        super(SinusoidaWyprostowanaDwupolowkowo, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p))
        poczatkowe_zera.fill(0)
        t = np.arange(0, self._czas_trwania_czystego_sygnalu + self.f_p, self.f_p)
        return np.append(poczatkowe_zera, np.abs(self.A * np.sin(2*np.pi/self.T * (t-self.t1))))


class Prostokat(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania, wspolczynnik_wypelnienia):
        super(Prostokat, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)
        self.k_w = wspolczynnik_wypelnienia
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p))
        poczatkowe_zera.fill(0)
        x = np.empty(self._ilosc_probek_wlasciwych)
        for i in range(self._ilosc_probek_wlasciwych):
            t = self.t1 + self.f_p * i
            k = int((i * self.f_p)/self.T)
            arg0 = (k*self.T + self.t1)
            arg1 = (self.k_w*self.T + k*self.T + self.t1)
            if arg0 <= t < arg1:
                x[i] = self.A
            else:
                x[i] = 0
        return np.append(poczatkowe_zera, x)


class ProstokatSymetryczny(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania, wspolczynnik_wypelnienia):
        super(ProstokatSymetryczny, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)
        self.k_w = wspolczynnik_wypelnienia
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p))
        poczatkowe_zera.fill(0)
        x = np.empty(self._ilosc_probek_wlasciwych)
        for i in range(self._ilosc_probek_wlasciwych):
            t = self.t1 + self.f_p * i
            k = int((i * self.f_p)/self.T)
            arg0 = (k*self.T + self.t1)
            arg1 = (self.k_w*self.T + k*self.T + self.t1)
            if arg0 <= t < arg1:
                x[i] = self.A
            else:
                x[i] = -self.A
        return np.append(poczatkowe_zera, x)


class Trojkat(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania, wspolczynnik_wypelnienia):
        super(Trojkat, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)
        self.k_w = wspolczynnik_wypelnienia
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p))
        poczatkowe_zera.fill(0)
        x = np.empty(self._ilosc_probek_wlasciwych)
        for i in range(self._ilosc_probek_wlasciwych):
            t = self.t1 + self.f_p * i
            k = int((i * self.f_p)/self.T)
            arg0 = (k*self.T + self.t1)
            arg1 = (self.k_w*self.T + k*self.T + self.t1)
            wspolczynnik_do_wyliczania_x = (t - k * self.T - self.t1)
            if arg0 <= t < arg1:
                x[i] = self.A / (self.k_w * self.T) * wspolczynnik_do_wyliczania_x
            else:
                x[i] = -self.A / (self.T * (1 - self.k_w)) * wspolczynnik_do_wyliczania_x + self.A / (1 - self.k_w)
        return np.append(poczatkowe_zera, x)


class SkokJednostkowy(SygnalCiagly):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania, t_skoku):
        super(SkokJednostkowy, self).\
            __init__(amplituda, czas_poczatkowy, czas_trwania, okres, f_probkowania)
        self.t_s = t_skoku
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        poczatkowe_zera = np.empty(int(self.t1/self.f_p)+int((self.t_s-self.t1)/self.f_p))
        poczatkowe_zera.fill(0)
        poczatkowe_zera[-1] = self.A/2
        koncowe_zera = np.empty(int((self.d-self.t_s+self.f_p)/self.f_p))
        koncowe_zera.fill(self.A)
        return np.append(poczatkowe_zera, koncowe_zera)


class S1(SygnalCiagly):
    def __init__(self):
        super(S1, self).\
            __init__(7, 0, 1/16 * 16 - 0.00001, 0.5, 1/16)
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        t = np.arange(16) * (1/16)
        return 2 * np.sin(np.pi * t + np.pi / 2) + 5 * np.sin(4 * np.pi * t + np.pi/2)


class S2(SygnalCiagly):
    def __init__(self):
        super(S2, self).\
            __init__(7, 0, 1/16 * 16 - 0.00001, 0.5, 1/16)
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        t = np.arange(16) * (1/16)
        return 2 * np.sin(np.pi * t) + np.sin(2 * np.pi * t) + 5 * np.sin(4 * np.pi * t)


class S3(SygnalCiagly):
    def __init__(self):
        super(S3, self).\
            __init__(7, 0, 1/16 * 16 - 0.00001, 0.5, 1/16)
        self.y = self._generuj_probki()

    def _generuj_probki(self):
        t = np.arange(16) * (1/16)
        return 5 * np.sin(np.pi * t) + np.sin(4 * np.pi * t)
