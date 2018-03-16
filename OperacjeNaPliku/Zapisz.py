def zapisz(sygnal, name="wykres.txt"):
    file = open(name, "w")
    try:
        file.write(str(sygnal.t1))  # t1
    except Exception:
        file.write(str(sygnal.n1))  # n1
    file.write('\n')
    file.write(str(sygnal.f_p))  # f_p
    file.write('\n')
    file.write('complex')  # real/complex
    file.write('\n')
    file.write(str(int(sygnal.d / sygnal.f_p)+1))  # size
    file.write('\n')
    for y in sygnal.y:
        file.write('%.2f' % y)
        file.write('\n')
    file.close()
