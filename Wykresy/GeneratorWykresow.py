from Generator import SygnalDyskretny, SygnalCiagly
import matplotlib.pyplot as plt

sig = SygnalCiagly.Prostokat(10, 0.4, 10, 0.5, 0.01, 0.75)  # nie dziala argument z czasem poczatkowym
plt.plot(sig.generuj())
plt.show()
