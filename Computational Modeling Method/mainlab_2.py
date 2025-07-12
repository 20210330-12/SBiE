import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import mainlab_func as ref

# 초기조건: 모두 0 (인산화된 형태 없음)
y0 = [0, 0, 0, 0, 0]
t = np.linspace(0, 5000, 5000)

sol = odeint(ref.MAPK_model, y0, t, args=(ref.params,))
# sol은 2차원 배열임. 행: 시간 (t), 열: 각 변수 (MKKK_P 같은 것들)
# print(sol)
print(sol[-1, 0])
print(sol[4999, 0])
MKKK_P = sol[:, 0] # :는 전체 시간, 즉 0부터 5000까지 나타내는 거고, 0은 dMKKK_P 나타냄
MKK_P = sol[:, 1]
MKK_PP = sol[:, 2]
MAPK_P = sol[:, 3]
MAPK_PP = sol[:, 4]

plt.figure(figsize=(10, 9))
plt.plot(t, MAPK_PP, label='[MAPK-PP]')
plt.plot(t, MKK_PP, label='[MKK-PP]')
plt.plot(t, MKKK_P, label='[MKKK-P]')
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.title('MAPK signaling pathway simulation')
plt.legend()
plt.grid(True)
plt.xlim(0, 5000)
plt.ylim(0, 300)
plt.show()
