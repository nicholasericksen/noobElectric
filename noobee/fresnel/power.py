from __future__ import division
import numpy as np
import math
import matplotlib.pyplot as plt

n1 = 1.0
n2 = 1.5

theta_i = np.arange(0,90,1)
print theta_i
for index, theta in  enumerate(theta_i):
    print "Theta", theta
    Rs = math.pow(math.fabs((n1*math.cos(theta) - n2*math.sqrt(1 - math.pow((n1/n2)*math.sin(theta), 2))) / (n1*math.cos(theta) + n2*math.sqrt(1-math.pow((n1/n2)*math.sin(theta),2)))),2)
    print "Index", index
    plt.scatter(theta_i[index], Rs)
    print Rs

plt.show()
