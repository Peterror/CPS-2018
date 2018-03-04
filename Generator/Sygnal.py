import numpy as np


# Klasy bazowe

class Sygnal(object):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania):
        self.A = amplituda
        self.t1 = czas_poczatkowy
        self.d = czas_trwania


# Klasy dziedziczace

class SzumJednostajny(Sygnal):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania):
        super(SzumJednostajny, self).__init__(amplituda, czas_poczatkowy, czas_trwania)

    def generuj(self, f_probkowania):
        raise NotImplementedError()


class SzumGaussowski(Sygnal):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania):
        super(SzumGaussowski, self).__init__(amplituda, czas_poczatkowy, czas_trwania)

    def generuj(self, f_probkowania):
        raise NotImplementedError()


class Sinusoida(Sygnal):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania):
        super(Sinusoida, self).__init__(amplituda, czas_poczatkowy, czas_trwania)

    def generuj(self, f_probkowania):
        raise NotImplementedError()


class SinusoidaWyprostowanaJednopolowkowo(Sygnal):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania):
        super(SinusoidaWyprostowanaJednopolowkowo, self).__init__(amplituda, czas_poczatkowy, czas_trwania)

    def generuj(self, f_probkowania):
        raise NotImplementedError()


class SinusoidaWyprostowanaDwupolowkowo(Sygnal):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania):
        super(SinusoidaWyprostowanaDwupolowkowo, self).__init__(amplituda, czas_poczatkowy, czas_trwania)

    def generuj(self, f_probkowania):
        raise NotImplementedError()


class Prostokat(Sygnal):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania):
        super(Prostokat, self).__init__(amplituda, czas_poczatkowy, czas_trwania)

    def generuj(self, f_probkowania, wypelnienie):
        raise NotImplementedError()


class ProstokatSymetryczny(Sygnal):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania):
        super(ProstokatSymetryczny, self).__init__(amplituda, czas_poczatkowy, czas_trwania)

    def generuj(self, f_probkowania):
        raise NotImplementedError()


class Trojkat(Sygnal):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania):
        super(Trojkat, self).__init__(amplituda, czas_poczatkowy, czas_trwania)

    def generuj(self, f_probkowania):
        raise NotImplementedError()


class SkokJednostkowy(Sygnal):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania):
        super(SkokJednostkowy, self).__init__(amplituda, czas_poczatkowy, czas_trwania)

    def generuj(self, f_probkowania):
        raise NotImplementedError()


# Dyskretne sygnaly

class ImpulsJednostkowy(Sygnal):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania):
        super(ImpulsJednostkowy, self).__init__(amplituda, czas_poczatkowy, czas_trwania)

    def generuj(self, f_probkowania):
        raise NotImplementedError()


class SzumImpulsowy(Sygnal):
    def __init__(self, amplituda, czas_poczatkowy, czas_trwania):
        super(SzumImpulsowy, self).__init__(amplituda, czas_poczatkowy, czas_trwania)

    def generuj(self, f_probkowania):
        raise NotImplementedError()


