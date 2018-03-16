from Generator.SygnalCiagly import SygnalCiaglyNieokreslony
import numpy as np


def wczytaj(name="wykres.txt"):
    file = open(name, "r")

    t1 = float(file.readline())  # t1
    f_p = float(file.readline())  # f_p
    file.readline()  # real/complex
    size = int(file.readline())  # probki
    y = np.empty(size)
    data = file.readline()  # probki
    i = 0
    while data != '':
        y[i] = float(data)
        i += 1
        data = file.readline()  # probki
    file.close()
    x = np.arange(0, size*f_p, f_p)
    return SygnalCiaglyNieokreslony(x, y)
