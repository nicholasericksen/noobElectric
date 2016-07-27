import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import math

t = range(0, 20, 1)
volts = [-4.3, 1.2, -0.6, -0.9, 3.4, -2.7, 4.3, 0.1, -3.2, -4.6, 1.8, 3.6, 2.4, -2.7, 0.5, -0.5, -3.7, 2.1, -4.1, -0.4]



f = interp1d(t,volts, kind='cubic')
tnew = np.arange(0, 19, 0.1)
vnew = f(tnew)


def QuantizedLevels(xmin, xmax, bits):
        levels = (xmax - xmin) / math.pow(2, bits)
        qLevels = np.arange(xmin, xmax, levels)
        return qLevels
vlevels1 = QuantizedLevels(-5, 5, 4)
vlevels2 = QuantizedLevels(-5, 5, 8)

qVolts = []
qVolts2 = []

for volt in volts:
      qVolts.append(min(vlevels1, key=lambda x:abs(x-volt)))
      qVolts2.append(min(vlevels2, key=lambda x:abs(x-volt)))

f2 = interp1d(t, qVolts2)
errorRaw = f2(tnew)

error = abs(errorRaw - vnew)


plt.plot(t, volts, 'gv', label='Sampled')
plt.plot(tnew, vnew, label='Fitted')
#plt.step(t, qVolts, 'rv', label='4 bit')
plt.step(t, qVolts2, 'bv', label='8 bit')
plt.plot(tnew, error, label='Error')


plt.title('A-D Conversion', fontsize=18)
plt.xlabel('Time [ms]', fontsize=14)
plt.ylabel('Vsampled [volts]', fontsize=14)
plt.legend(loc='upper right')
plt.show()

