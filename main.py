from Generator.SygnalCiagly import Trojkat, SzumORozkladzieJednostajnym, SzumGaussowski, SkokJednostkowy, \
    SinusoidaWyprostowanaJednopolowkowo, SinusoidaWyprostowanaDwupolowkowo, ProstokatSymetryczny, Sinusoida, Prostokat,\
    SygnalCiaglyNieokreslony
from Generator.SygnalDyskretny import SygnalDyskretny, SzumImpulsowy, ImpulsJednostkowy
from Wykresy.GeneratorWykresow import generuj_wykres, generuj_histogram
from OperacjeNaPliku import Wczytaj, Zapisz


def wypisz_dostepne_sygnaly():
    print("(S0) sygnał z pliku;")
    print("(S1) szum o rozkładzie jednostajnym;")
    print("(S2) szum gaussowski;")
    print("(S3) sygnał sinusoidalny;")
    print("(S4) sygnał sinusoidalny wyprostowany jednopołówkowo;")
    print("(S5) sygnał sinusoidalny wyprostowany dwupołówkowo;")
    print("(S6) sygnał prostokątny;")
    print("(S7) sygnał prostokątny symetryczny;")
    print("(S8) sygnał trójkątny;")
    print("(S9) skok jednostkowy;")
    print("(S10) impuls jednostkowy;")
    print("(S11) szum impulsowy;")


def wypisz_dostepne_dzialania():
    print("(D1) dodawanie;")
    print("(D2) odejmowanie;")
    print("(D3) mnożenie;")
    print("(D4) dzielenie;")


def wygeneruj_sygnal():
    print("Który sygnał chcesz generować?")
    wypisz_dostepne_sygnaly()
    wybrany_sygnal = input("Generuj sygnał o kodzie S")
    parametry = ['amplituda ', 'czas_poczatkowy ', 'czas_trwania ', 'okres ', 'f_probkowania ']
    dyskretne_parametry = ['amplituda ', 'numer_pierwszej_probki ', 'czas_trwania ', 'f_probkowania ']
    opcje = {
        '0':  [Wczytaj.wczytaj, ['Nazwa pliku ']],
        '1':  [SzumORozkladzieJednostajnym, parametry],
        '2':  [SzumGaussowski, parametry],
        '3':  [Sinusoida, parametry],
        '4':  [SinusoidaWyprostowanaJednopolowkowo, parametry],
        '5':  [SinusoidaWyprostowanaDwupolowkowo, parametry],
        '6':  [Prostokat, parametry + ['wspolczynnik_wypelnienia ']],
        '7':  [ProstokatSymetryczny, parametry + ['wspolczynnik_wypelnienia ']],
        '8':  [Trojkat, parametry + ['wspolczynnik_wypelnienia ']],
        '9':  [SkokJednostkowy, parametry + ['czas_skoku ']],
        '10': [ImpulsJednostkowy, dyskretne_parametry + ['numer próbki skoku ']],
        '11': [SzumImpulsowy, dyskretne_parametry + ['prawdopodobieństwo skoku ']],
    }
    if opcje[wybrany_sygnal] is None:
        raise NotImplementedError

    argumenty = []
    print("Podaj parametry sygnału:")
    for nazwa_parametru in opcje[wybrany_sygnal][1]:
        wartosc = input(nazwa_parametru)
        try:
            argumenty += [int(wartosc)]
        except ValueError:
            try:
                argumenty += [float(wartosc)]
            except ValueError:
                argumenty += [wartosc]
    obiekt_sygnalu = opcje[wybrany_sygnal][0](*argumenty)

    return obiekt_sygnalu


def wykonaj_dzialanie_na_sygnale(sygnal):
    def _dodaj(uklad_xy_a):
        uklad_xy_b = wygeneruj_sygnal()
        return uklad_xy_b+uklad_xy_a

    def _odejmij(uklad_xy_a):
        uklad_xy_b = wygeneruj_sygnal()
        return uklad_xy_a-uklad_xy_b

    def _pomnoz(uklad_xy_a):
        uklad_xy_b = wygeneruj_sygnal()
        return uklad_xy_a*uklad_xy_b

    def _podziel(uklad_xy_a):
        uklad_xy_b = wygeneruj_sygnal()
        return uklad_xy_a/uklad_xy_b

    print("Jakie działania wykonać na tym sygnale?")
    wypisz_dostepne_dzialania()
    wybrane_dzialanie = input("Wykonaj działanie D")

    opcje = {
        '1': _dodaj,
        '2': _odejmij,
        '3': _pomnoz,
        '4': _podziel,
    }
    if opcje[wybrane_dzialanie] is None:
        raise NotImplementedError
    sygnal_wynikowy = opcje[wybrane_dzialanie](sygnal)
    return sygnal_wynikowy


def wykonaj_operacje_programu(sygnal):
    def local_zapisz_sygnal_do_pliku():
        Zapisz.zapisz(sygnal)
        return True

    def local_wyswietl_wykres():
        if isinstance(sygnal, SygnalDyskretny):
            generuj_histogram(sygnal)
        else:
            generuj_wykres(sygnal)
        return True

    def local_kontynuuj():
        return False

    print("Co wykonać przed działaniami na sygnale?")
    print("(W1) Zapisanie wygenerowanego sygnalu do pliku;")
    print("(W2) Wyświetl wykres;")
    print("(W3) KONTYNUUJ;")

    opcje = {
        '1': local_zapisz_sygnal_do_pliku,
        '2': local_wyswietl_wykres,
        '3': local_kontynuuj,
    }
    wybrany_wariant = input("Wykonaj wariant W")
    if opcje[wybrany_wariant] is None:
        raise NotImplementedError
    return opcje[wybrany_wariant]()


def main():
    sygnal = wygeneruj_sygnal()
    while True:
        wykonaj_operacje_programu(sygnal)
        sygnal = wykonaj_dzialanie_na_sygnale(sygnal)


if __name__ == "__main__":
    main()
