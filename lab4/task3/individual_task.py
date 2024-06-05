from math import log
import numpy as np
import matplotlib.pyplot as plt


class LogFunction:
    def __init__(self, eps, max_iter):
        self.eps = eps
        self.max_iter = max_iter

    def log_fun(self, x):
        result = 0.
        accuracy = self.eps + 1
        iterations_count = 1

        while accuracy >= self.eps and iterations_count <= self.max_iter:
            result += -1 * x ** iterations_count / iterations_count
            accuracy = abs(log(1 - x) - result)
            iterations_count += 1

        return result, iterations_count


log_func = LogFunction(1e-5, 1000)

x_values = np.linespace(0.001, 0.999, 1000)
function_values = [log_func.log_fun(x)[0] for x in x_values]

# Plot the function
plt.plot(x_values, function_values, label='log(1-x)')
plt.xlabel('x')
plt.ylabel('log(1-x)')
plt.title('Plot of log(1-x)')
plt.grid(True)
plt.legend()
plt.show()
