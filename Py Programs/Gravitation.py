import matplotlib.pyplot as plt
import numpy as np
r = np.linspace(1e6, 4e8, 100)
G = 6.67e-11
m1 = 5.972e24
m2 = 7.348e22

F = G * m1 * m2 / r**2
plt.plot(r, F)
plt.xlabel('Distance')
plt.ylabel('Force')
plt.title("Distance is to force")

#plt.xscale("log")
plt.yscale("log")

plt.grid()
plt.show()