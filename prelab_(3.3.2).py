import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# X-P의 Michaelis-Menten equation
# Assume all the kinetic constant parameter values (k) as 1
def dXdt(XP, t, I, Y):
    k1 = 1
    k2 = 1
    Km1 = 1
    Km2 = 1
    dXP = k1 * Y * (1 - XP) / (Km1 + (1 - XP)) - k2 * I * XP / (Km2 + XP)
    return dXP

# 초기조건 필요, XP는 처음에는 없을 테니까 (X로부터 만들어질 거니까) 0으로
XP0 = 0.0

# Y와 I 값 설정 -> 나중에 바꿔가면서 steady-state 볼 것임
I = 1
Y = 1

# ODE 식 세우기
t = np.linspace(0, 20, 200)
XP = odeint(dXdt, XP0, t, args=(I, Y))

# 그래프 그리기
plt.plot(t, XP, label='Concentration (X-P)')
plt.title('Michaelis-Menton (Prelab 3.4)')
plt.xlabel('Time')
plt.ylabel('Concentration (X-P)')
plt.xlim(0, 20)

plt.show()