import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def iFFL_ode(X, t, k6):
    XP, YP, ZP = X
    k = Km = 1
    I = Ex = Ey = 1
    dXP = k * I * (1 - XP) / (Km + (1 - XP)) - k * Ex * XP / (Km + XP)
    dYP = k * XP * (1 - YP) / (Km + (1 - YP)) - k * Ey * YP / (Km + YP)
    dZP = k * XP * (1 - ZP) / (Km + (1 - ZP)) - k6 * YP * ZP / (Km + ZP)
    return [dXP, dYP, dZP]

X0 = [0, 0, 0]
t = np.linspace(0, 10, 300)
k6_values = [1, 10, 100]

fig, axes = plt.subplots(1, 3, figsize=(9, 10), sharey=True)

for ax, k6 in zip(axes, k6_values):
    sol = odeint(iFFL_ode, X0, t, args=(k6, ))
    XP, YP, ZP = sol.T
    ax.plot(t, XP, label='[X-P]')
    ax.plot(t, YP, label='[Y-P]')
    ax.plot(t, ZP, label='[Z-P]')
    ax.set_title(f'kY-|Z = {k6}')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Concentration')
    ax.legend()
    ax.grid(True)
    ax.set_xlim(0, 10)
    ax.set_xticks([0, 5, 10])
    ax.set_ylim(0, 1)
    ax.set_yticks(np.arange(0, 1.1, 0.1))

plt.suptitle('Feedforward Circuit')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
