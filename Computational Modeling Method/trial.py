import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import mainlab_func as ref

# 이전에 작성한 MAPK_model 함수는 생략

# 고정 파라미터 (V1, n, Ki, K1, ...), Ki는 나중에 바꿀 예정
base_params = [
    2.5, 1, 9, 10,       # V1, n, Ki, K1
    0.25, 8,
    0.025, 15,
    0.025, 15,
    0.75, 15,
    0.75, 15,
    0.025, 15,
    0.025, 15,
    0.5, 15,
    0.5, 15
]

y0 = [0, 0, 0, 0, 0]

# 시간 (0~12000초 = 200분)
t = np.linspace(0, 12000, 4000)
# t = np.linspace(0, 5000, 5000)

# steady-state 시작 시점 (예: 100분 이후 = 6000초)
steady_state_start = 6000
# steady_state_start = 1500
steady_state_idx = np.where(t >= steady_state_start)[0][0]

# 4.4-1) Ki 변화에 따른 MAPK-PP 최대/최소 농도 구하기
# Ki를 로그 스케일로 2^(-3) ~ 2^(3) 범위로 변화
log2_Ki_values = np.arange(-10, 10.1, 0.1)
Ki_values = 2 ** log2_Ki_values

MAPK_PP_max_Ki = []
MAPK_PP_min_Ki = []

for Ki in Ki_values:
    params = base_params.copy()
    params[2] = Ki  # Ki 값 변경
    sol = odeint(ref.MAPK_model, y0, t, args=(params,))
    MAPK_PP_steady = sol[steady_state_idx:, 4]
    MAPK_PP_max_Ki.append(np.max(MAPK_PP_steady))
    MAPK_PP_min_Ki.append(np.min(MAPK_PP_steady))

# 4.4-2) V1 변화에 따른 MAPK-PP 최대/최소 농도 구하기
# V1도 로그 스케일로 2^(-3) ~ 2^(3) 범위로 변화
log2_V1_values = np.arange(-10, 10.1, 0.1)
V1_values = 2 ** log2_V1_values

MAPK_PP_max_V1 = []
MAPK_PP_min_V1 = []

for V1 in V1_values:
    params = base_params.copy()
    params[0] = V1  # V1 값 변경
    sol = odeint(ref.MAPK_model, y0, t, args=(params,))
    MAPK_PP_steady = sol[steady_state_idx:, 4]
    MAPK_PP_max_V1.append(np.max(MAPK_PP_steady))
    MAPK_PP_min_V1.append(np.min(MAPK_PP_steady))

# 4.4-3) 진동 발생 범위 찾기 (Ki 기준)
MAPK_PP_max_Ki = np.array(MAPK_PP_max_Ki)
MAPK_PP_min_Ki = np.array(MAPK_PP_min_Ki)
diff_Ki = MAPK_PP_max_Ki - MAPK_PP_min_Ki
oscillation_indices = np.where(diff_Ki > 1e-2)[0]  # 임계값 0.01 이상 차이 진동으로 간주
oscillation_range_Ki = (Ki_values[oscillation_indices[0]], Ki_values[oscillation_indices[-1]])

print(f"Oscillation range of Ki: {oscillation_range_Ki}")

# 4.4-4) 그래프 그리기

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Ki 변화에 따른 최대/최소 MAPK-PP 농도 (로그 x축)
axes[0].plot(Ki_values, MAPK_PP_max_Ki, label='Max')
axes[0].plot(Ki_values, MAPK_PP_min_Ki, label='Min')
axes[0].set_xscale('log', base=2)
axes[0].set_xlabel('Ki (log2 scale)')
axes[0].set_ylabel('MAPK-PP Concentration')
axes[0].set_title('MAPK-PP max/min vs Ki')
axes[0].legend()
axes[0].grid(True, which='both', ls='--')

# V1 변화에 따른 최대/최소 MAPK-PP 농도 (로그 x축)
axes[1].plot(V1_values, MAPK_PP_max_V1, label='Max')
axes[1].plot(V1_values, MAPK_PP_min_V1, label='Min')
axes[1].set_xscale('log', base=2)
axes[1].set_xlabel('V1 (log2 scale)')
axes[1].set_ylabel('MAPK-PP Concentration')
axes[1].set_title('MAPK-PP max/min vs V1')
axes[1].legend()
axes[1].grid(True, which='both', ls='--')

plt.suptitle('Sustained Oscillations in MAPK Cascade')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
