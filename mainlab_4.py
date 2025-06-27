import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import mainlab_func as ref

# 초기조건 (모두 0)
y0 = [0, 0, 0, 0, 0]

# 시간 (0~5000 ms)
t = np.linspace(0, 12000, 8000)

# K_i
log2_Kis = np.arange(-10, 10.1, 0.1)
Kis = 2 ** log2_Kis

MAPK_PP_max_Ki = []
MAPK_PP_min_Ki = []

for Ki in Kis:
    change_Ki_params = ref.params.copy()
    change_Ki_params[2] = Ki
    sol = odeint(ref.MAPK_model, y0, t, args=(change_Ki_params,))
    # steady-state는 1500ms 이후라고 가정, 내 임의..
    MAPK_PP_max_Ki.append(np.max(sol[1500:, 4]))
    MAPK_PP_min_Ki.append(np.min(sol[1500:, 4]))


# V_1
log2_V1s = np.arange(-10, 10.1, 0.1)
V1s = 2 ** log2_V1s

MAPK_PP_max_V1 = []
MAPK_PP_min_V1 = []

for V1 in V1s:
    change_V1_params = ref.params.copy()
    change_V1_params[0] = V1
    sol = odeint(ref.MAPK_model, y0, t, args=(change_V1_params,))
    MAPK_PP_max_V1.append(np.max(sol[1500:, 4]))
    MAPK_PP_min_V1.append(np.min(sol[1500:, 4]))

MAPK_PP_max_Ki = np.array(MAPK_PP_max_Ki)
MAPK_PP_min_Ki = np.array(MAPK_PP_min_Ki)
MAPK_PP_max_V1 = np.array(MAPK_PP_max_V1)
MAPK_PP_min_V1 = np.array(MAPK_PP_min_V1)

fig, axes = plt.subplots(2, 1, figsize=(9, 10), sharex=True)

# Ki 그래프
axes[0].plot(log2_Kis, MAPK_PP_max_Ki, label='Max')
axes[0].plot(log2_Kis, MAPK_PP_min_Ki, label='Min')
axes[0].set_title('MAPK simulation depending on Ki')
# axes[0].set_xscale('log', base=2)
axes[0].set_xlabel('log2 Ki')
axes[0].set_ylabel('Concentration')
axes[0].legend()
axes[0].grid(True)

# V1 그래프
axes[1].plot(log2_V1s, MAPK_PP_max_V1, label='Max')
axes[1].plot(log2_V1s, MAPK_PP_min_V1, label='Min')
axes[1].set_xlabel('log2 V1')
axes[1].set_ylabel('Concentration')
axes[1].set_title('MAPK simulation depending on V1')
axes[1].legend()
axes[1].grid(True)

plt.xlim(-10, 10)
plt.tight_layout(rect=[0, 0, 1, 0.95])


# oscillation 나타내는 범위 찾기
diff_Ki = MAPK_PP_max_Ki - MAPK_PP_min_Ki
oscillation = np.where(diff_Ki > 1e-2)[0]  # 임계값 0.01 이상 차이 진동으로 간주
oscillation_range_Ki = (Kis[oscillation[0]], Kis[oscillation[-1]])
print(f"Oscillation range of Ki: {oscillation_range_Ki}")


plt.show()