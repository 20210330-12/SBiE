import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import mainlab_func as ref

# 초기조건 (모두 0)
y0 = [0, 0, 0, 0, 0]

# 시간 (0~5000 ms)
t = np.linspace(0, 5000, 5000)

# V1 값 범위 (0부터 3까지 0.1 간격)
V1_values = np.arange(0, 3.1, 0.1)

# 결과 저장용 리스트
MKKK_P_max = []
MKK_PP_max = []
MAPK_PP_max = []

for V1 in V1_values:
    change_v1_params = ref.params.copy()
    change_v1_params[0] = V1
    sol = odeint(ref.MAPK_model, y0, t, args=(change_v1_params,))
    # steady-state는 1500ms 이후라고 가정, 내 임의..
    MKKK_P_max.append(np.max(sol[1500:, 0]))
    MKK_PP_max.append(np.max(sol[1500:, 2]))
    MAPK_PP_max.append(np.max(sol[1500:, 4]))

# 배열로 변환
MKKK_P_max = np.array(MKKK_P_max)
MKK_PP_max = np.array(MKK_PP_max)
MAPK_PP_max = np.array(MAPK_PP_max)

MKKK_P_norm = MKKK_P_max / MKKK_P_max.max()
MKK_PP_norm = MKK_PP_max / MKK_PP_max.max()
MAPK_PP_norm = MAPK_PP_max / MAPK_PP_max.max()

fig, axes = plt.subplots(2, 1, figsize=(9, 10), sharex=True)

# 원본 자극-반응 곡선
axes[0].plot(V1_values, MAPK_PP_max, label='MAPK-PP')
axes[0].plot(V1_values, MKK_PP_max, label='MKK-PP')
axes[0].plot(V1_values, MKKK_P_max, label='MKKK-P')
axes[0].set_xlabel('V1')
axes[0].set_ylabel('Concentration')
axes[0].set_title('MAPK simulation depending on V1')
axes[0].legend()
axes[0].grid(True)

# 정규화된 자극-반응 곡선
axes[1].plot(V1_values, MAPK_PP_norm, label='MAPK-PP (normalized)')
axes[1].plot(V1_values, MKK_PP_norm, label='MKK-PP (normalized)')
axes[1].plot(V1_values, MKKK_P_norm, label='MKKK-P (normalized)')
axes[1].set_xlabel('V1')
axes[1].set_ylabel('Concentration (Normalized)')
axes[1].set_title('MAPK simulation depending on V1 (Normalized)')
axes[1].legend()
axes[1].grid(True)

plt.xlim(0, 3)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()