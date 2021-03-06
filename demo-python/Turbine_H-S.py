"""
 H-S(Mollier) Diagram of Steam Turbine Expansion

 4 lines:

    1  Isobar line:p inlet
    2  Isobar line:p outlet
    3  isentropic line:  (p inlet ,t inlet h inlet,s inlet), (p outlet,s inlet)
    4  Expansion line: inlet,outlet

License: this code is in the public domain

Author:   Cheng Maohua
Email:    cmh@seu.edu.cn

Last modified: 2018.11.28

"""
from seuif97 import ief, ishd, ph2t, ps2h, pt2h, pt2s

import matplotlib.pyplot as plt
import numpy as np


class Turbine(object):

    def __init__(self, pin, tin, pex, tex):
        self.pin = pin
        self.tin = tin
        self.pex = pex
        self.tex = tex

    def analysis(self):
        self.ef = ief(self.pin, self.tin, self.pex, self.tex)
        self.his = ishd(self.pin, self.tin, self.pex)

        self.hin = pt2h(self.pin, self.tin)
        self.sin = pt2s(self.pin, self.tin)

        self.hex = pt2h(self.pex, self.tex)
        self.sex = pt2s(self.pex, self.tex)

    def expansionline(self):
        sdelta = 0.01

        # 1 Isobar pin
        s_isopin = np.array([self.sin - sdelta, self.sin + sdelta])
        h_isopin = np.array([ps2h(self.pin, s_isopin[0]),
                             ps2h(self.pin, s_isopin[1])])

        # 2 Isobar pex
        s_isopex = np.array([s_isopin[0], self.sex + sdelta])
        h_isopex = np.array([ps2h(self.pex, s_isopex[0]),
                             ps2h(self.pex, s_isopex[1])])

        # 3 isentropic lines
        h_isos = np.array([self.hin, self.hin-self.his])
        s_isos = np.array([self.sin, self.sin])

        # 4 expansion Line
        h_expL = np.array([self.hin, self.hex])
        s_expL = np.array([self.sin, self.sex])

        # plot lines
        plt.figure(figsize=(6, 8))
        plt.title("H-S(Mollier) Diagram of Steam Turbine Expansion")
        plt.plot(s_isopin, h_isopin, 'b-')  # Isobar line: pin
        plt.plot(s_isopex, h_isopex, 'b-')  # Isobar line: pex

        plt.plot(s_isos, h_isos, 'ys-')  # isoentropic line:
        plt.plot(s_expL, h_expL, 'r-', label='Expansion Line')
        plt.plot(s_expL, h_expL, 'rs')

        _title = 'The isentropic efficiency = ' + \
            r'$\frac{h_1-h_2}{h_1-h_{2s}}$' + '=' + \
            '{:.2f}'.format(self.ef) + '%'

        plt.legend(loc="center", bbox_to_anchor=[
                   0.6, 0.9], ncol=2, shadow=True, title=_title)

        # annotate the inlet and exlet
        txt = "h1(%.2f,%.2f)" % (self.pin, self.tin)
        plt.annotate(txt,
                     xy=(self.sin, self.hin), xycoords='data',
                     xytext=(+1, +10), textcoords='offset points', fontsize=10,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

        txt = "h2(%.2f,%.2f)" % (self.pex, self.tex)
        plt.annotate(txt,
                     xy=(self.sex, self.hex), xycoords='data',
                     xytext=(+1, +10), textcoords='offset points', fontsize=10,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
       # annotate h2s
        txt = "h2s(%.2f,%.2f)" % (self.pex, ph2t(self.pex, h_isos[1]))
        plt.annotate(txt,
                     xy=(self.sin, h_isos[1]), xycoords='data',
                     xytext=(+1, +10), textcoords='offset points', fontsize=10,
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

        plt.xlabel('s(kJ/(kg.K))')
        plt.ylabel('h(kJ/kg)')
        plt.grid()
        plt.show()

    def __str__(self):
        result = ('\n  Inlet(p, t)  {:>6.2f}MPa {:>6.2f}°C \n  Exlet(p, t) {:>6.2f}MPa {:>6.2f}°C \nThe isentropic efficiency: {:>5.2f}%'
                  .format(self.pin, self.tin, self.pex, self.tex, self.ef))
        return result


if __name__ == '__main__':
    pin, tin = 16.0, 535.0
    pex, tex = 3.56, 315.0
    tb1 = Turbine(pin, tin, pex, tex)
    tb1.analysis()
    print(tb1)
    tb1.expansionline()
