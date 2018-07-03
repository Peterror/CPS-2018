import matplotlib.pyplot as plt
import math


def generuj_ReIm(frequency_bins):
    plt.subplot(2, 1, 1)
    plt.title("Re")
    plt.plot([fb[0] for fb in frequency_bins])  # x y

    plt.subplot(2, 1, 2)
    plt.title("Im")
    plt.plot([fb[1] for fb in frequency_bins])  # x y
    plt.show()

def generuj_odleglosc(frequency_bins):
    plt.subplot(2, 1, 1)
    plt.title("|Re+Im|")
    plt.plot([math.sqrt(fb[0]**2 + fb[1]**2) for fb in frequency_bins])  # x y

    plt.subplot(2, 1, 2)
    plt.title("Arg")
    plt.plot([fb[0] * fb[1] for fb in frequency_bins])  # x y
    plt.show()
