from math import log
import numpy as np
import matplotlib.pyplot as plt
from individual_task import log_fun


def log_math(x):
    return log(1-x)

x = np.arange(0.1, 1, 0.001, dtype=float)

f = np.vectorize(log_math)
y1 = f(x)
y2 = log_fun(x)

fig, ax = plt.subplots()

ax.grid(True)
ax.plot(x, y1, 'g')
ax.plot(x, y2, 'r')

plt.savefig('plot.jpg')
plt.show()
