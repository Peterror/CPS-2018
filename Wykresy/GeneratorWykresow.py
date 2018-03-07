from Generator import SygnalDyskretny, SygnalCiagly
import matplotlib.pyplot as plt


def test():
    config = (10, 0, 10, 1.5, 0.01)
    plt.plot(*SygnalCiagly.Sinusoida(*config).generuj_uklad_xy())
    plt.plot(*SygnalCiagly.SinusoidaWyprostowanaDwupolowkowo(*config).generuj_uklad_xy())
    plt.plot(*SygnalCiagly.SinusoidaWyprostowanaJednopolowkowo(*config).generuj_uklad_xy())
    plt.show()

    plt.plot(*SygnalCiagly.Prostokat(*config, 0.75).generuj_uklad_xy())
    plt.plot(*SygnalCiagly.ProstokatSymetryczny(*config, 0.75).generuj_uklad_xy())
    plt.show()

    plt.plot(*SygnalCiagly.Trojkat(*config, 0.5).generuj_uklad_xy())
    plt.show()

    plt.plot(*SygnalCiagly.SkokJednostkowy(*config, 1).generuj_uklad_xy(), '.-')
    plt.show()

    plt.plot(*SygnalCiagly.SzumORozkladzieJednostajnym(*config).generuj_uklad_xy())
    plt.show()

    plt.plot(*SygnalCiagly.SzumGaussowski(*config).generuj_uklad_xy())
    plt.show()
    pass


if __name__ == "__main__":
    print("Tego sie tak nie uruchamia")
    test()
