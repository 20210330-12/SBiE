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
    dXP = k1 * I * (1 - XP) / (Km1 + (1 - XP)) - k2 * Y * XP / (Km2 + XP)
    return dXP

# 초기조건 필요, XP는 처음에는 없을 테니까 (X로부터 만들어질 거니까) 0으로
XP0 = 0.0

# ODE 식 세우기
t = np.linspace(0, 20, 200)

# Y, I값 바꾸기
params = [(0.5, 1), (1, 1), (2, 1), (1, 0.5), (1, 2)]

plt.figure(figsize=(8,6))
for I_val, Y_val in params:
    XP = odeint(dXdt, XP0, t, args=(I_val, Y_val))
    plt.plot(t, XP, label=f'I={I_val}, Y={Y_val}')

# 그래프 그리기
plt.title('Michaelis-Menton (Prelab 3.3.4)')
plt.xlabel('Time')
plt.ylabel('Concentration (X-P)')
plt.xlim(0, 20)
plt.legend()

plt.show()

# I와 Y의 관계에 따라 농도가 수렴하는 지점이 다름
# (0.5, 1) 과 (1, 2) 처럼, Y의 농도가 2배 더 높은 경우는,
# 값이 같거나 1/2배 차이나는 경우보다
# X-P 농도가 더 낮은 값에서 수렴함 (당연함)