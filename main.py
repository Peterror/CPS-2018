from Generator.SygnalCiagly import Trojkat, SzumORozkladzieJednostajnym, SzumGaussowski, SkokJednostkowy, \
    SinusoidaWyprostowanaJednopolowkowo, SinusoidaWyprostowanaDwupolowkowo, ProstokatSymetryczny, Sinusoida, Prostokat,\
    SygnalCiaglyNieokreslony, SygnalCiagly
from Generator.SygnalDyskretny import SygnalDyskretny, SzumImpulsowy, ImpulsJednostkowy
from Wykresy.GeneratorWykresow import generuj_wykres, generuj_histogram, generuj_wykresy_nalozone
from OperacjeNaPliku import Wczytaj, Zapisz
import numpy as np


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
    print("(D0) POMIN TEN KROK;")
    print("(D1) dodawanie;")
    print("(D2) odejmowanie;")
    print("(D3) mnożenie;")
    print("(D4) dzielenie;")


def wypisz_dostepne_dzialania_kwantyzacji():
    print("(D0) POMIN TEN KROK;")
    print("(D1) kwantyzacja z obcieciem;")
    print("(D2) kwantyzacja z zaokragleniem;")
    print("(D3) ekstrapolacja 0 rzedu;")
    print("(D4) ekstrapolacja 1 rzedu;")
    print("(D5) ekstrapolacja sinc;")


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
        't':  0,  # testowa sinusoida
    }
    if opcje[wybrany_sygnal] is None:
        raise NotImplementedError

    if opcje[wybrany_sygnal] == 0:  # dla testow
        return Sinusoida(5, 0, 5, 1, 0.01)

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
    print("Średnia %f" % obiekt_sygnalu.srednia())
    print("Moc średnia %f" % obiekt_sygnalu.moc_srednia())
    print("Średnia bezwzględna %f" % obiekt_sygnalu.srednia_bezwzgledna())
    print("Wariancja wokół średniej %f" % obiekt_sygnalu.wariancja_wokol_sredniej())
    print("Wartość skuteczna %f" % obiekt_sygnalu.wartosc_skuteczna())
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

    def _nie_rob_nic(uklad_xy_a):
        return uklad_xy_a

    print("Jakie działania wykonać na tym sygnale?")
    wypisz_dostepne_dzialania()
    wybrane_dzialanie = input("Wykonaj działanie D")

    opcje = {
        '0': _nie_rob_nic,
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
    print("(W0) POMIŃ TEN KROK;")
    print("(W1) Zapisanie wygenerowanego sygnalu do pliku;")
    print("(W2) Wyświetl wykres;")

    opcje = {
        '0': local_kontynuuj,
        '1': local_zapisz_sygnal_do_pliku,
        '2': local_wyswietl_wykres,
    }
    wybrany_wariant = input("Wykonaj wariant W")
    if opcje[wybrany_wariant] is None:
        raise NotImplementedError
    return opcje[wybrany_wariant]()


def dzialania_kwantyzacji(sygnal):
    def _kwantyzacja_z_obcieciem(uklad_xy_a: SygnalCiagly):
        T_kw = float(input("T_kwantyzacji: "))
        n_kw = 2**int(input("2^n_kwantyzacji: "))
        sygnal_po_kwantyzacji = SygnalCiaglyNieokreslony(
            uklad_xy_a.x,
            uklad_xy_a.kwantyzacja_z_obcieciem(
                T_kwantyzacji=T_kw,
                n_kwantyzacji=n_kw),
            T_kw,
            n_kw
        )
        return sygnal_po_kwantyzacji

    def _kwantyzacja_z_zaokragleniem(uklad_xy_a: SygnalCiagly):
        T_kw = float(input("T_kwantyzacji: "))
        n_kw = 2**int(input("2^n_kwantyzacji: "))
        sygnal_po_kwantyzacji = SygnalCiaglyNieokreslony(
            uklad_xy_a.x,
            uklad_xy_a.kwantyzacja_z_zaokragleniem(
                T_kwantyzacji=T_kw,
                n_kwantyzacji=n_kw),
            T_kw,
            n_kw
            )
        return sygnal_po_kwantyzacji

    def _ekstrapolacja_0rzedu(uklad_xy_a):
        return uklad_xy_a

    def _ekstrapolacja_1rzedu(uklad_xy_a):
        return uklad_xy_a.ekstrapolacja_1rzedu()

    def _sinc(uklad_xy_a):
        return uklad_xy_a.sinc()

    def _nie_rob_nic(uklad_xy_a):
        return uklad_xy_a

    sygnaly = [sygnal]
    while True:
        print("Jakie działania wykonać na tym sygnale?")
        wypisz_dostepne_dzialania_kwantyzacji()
        wybrane_dzialanie = input("Wykonaj działanie D")

        opcje = {
            '0': _nie_rob_nic,
            '1': _kwantyzacja_z_obcieciem,
            '2': _kwantyzacja_z_zaokragleniem,
            '3': _ekstrapolacja_0rzedu,
            '4': _ekstrapolacja_1rzedu,
            '5': _sinc,
        }

        if opcje[wybrane_dzialanie] is None:
            raise NotImplementedError
        if opcje[wybrane_dzialanie] is _nie_rob_nic:
            break

        sygnaly += [opcje[wybrane_dzialanie](sygnaly[-1])]
        generuj_wykresy_nalozone([sygnaly[0], sygnaly[-1]])
        try:
            MSE = np.sum((sygnaly[0].y - sygnaly[-1].y)**2)/sygnaly[0].y.size
            SNR = 10*np.log10(np.sum(sygnaly[0].y**2)/MSE*sygnaly[0].y.size)
            PSNR = 10*np.log10(np.max(sygnaly[0].y)/MSE)
            MD = np.max(np.abs(sygnaly[0].y-sygnaly[-1].y))
            print("MSE = %f" % MSE)
            print("SNR = %f" % SNR)
            print("PSNR = %f" % PSNR)
            print("MD = %f" % MD)
        except ValueError:
            pass

    return sygnaly[-1]


def main():
    sygnal = wygeneruj_sygnal()
    while True:
        wykonaj_operacje_programu(sygnal)
        sygnal = dzialania_kwantyzacji(sygnal)
        sygnal = wykonaj_dzialanie_na_sygnale(sygnal)


if __name__ == "__main__":
    main()
