import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import mainlab_func as ref

y0 = [0, 0, 0, 0, 0]

# 시간 (0~12000초 = 200분)
t = np.linspace(0, 12000, 4000)

# 정상상태 시작 시점 (예: 100분 이후 = 6000초)
steady_state_start = 6000
steady_state_idx = np.where(t >= steady_state_start)[0][0]

# Ki 변화 (log2 스케일)
log2_Ki_values = np.arange(-10, 10.1, 0.1)
Ki_values = 2 ** log2_Ki_values

MAPK_PP_max_Ki = []
MAPK_PP_min_Ki = []

for Ki in Ki_values:
    params = ref.params.copy()
    params[2] = Ki
    sol = odeint(ref.MAPK_model, y0, t, args=(params,))
    MAPK_PP_steady = sol[steady_state_idx:, 4]
    MAPK_PP_max_Ki.append(np.max(MAPK_PP_steady))
    MAPK_PP_min_Ki.append(np.min(MAPK_PP_steady))



# 진동 발생 범위 찾기 (Ki 기준)
MAPK_PP_max_Ki = np.array(MAPK_PP_max_Ki)
MAPK_PP_min_Ki = np.array(MAPK_PP_min_Ki)
diff_Ki = MAPK_PP_max_Ki - MAPK_PP_min_Ki
# oscillation_indices = np.where(diff_Ki > 1e-2)[0]
# np.where(condition)함수 -> condition이 true인 요소들의 인덱스를 찾아 튜플 형태로 반환
# ex. diff_Ki가 [0.005, 0.02, 0.008, 0.03] 이라면,
# diff_Ki > 1e-2는 [False, True, False, True]
# np.where([False, True, False, True])의 결과는 (array([1, 3]),) 이 됨!

oscillation_indices = np.where(diff_Ki > 1)[0] # 이 '진동'의 기준값이 뭔지 모르겠음! 일단 나는 1로 했어. GPT는 1/100이래..
oscillation_range_Ki = (Ki_values[oscillation_indices[0]], Ki_values[oscillation_indices[-1]])
print(f"Oscillation range of Ki: {oscillation_range_Ki}")



# Ki_oscillation = oscillation_range_Ki[0] * 1.2  # 진동 구간 내 임의 값
Ki_oscillation = 1.5 # 내가 oscillation range 출력해보고 임의로 숫자 하나 고른거임
params_osc = ref.params.copy()
params_osc[2] = Ki_oscillation

t_long = np.linspace(0, 12000, 8000)
sol_osc = odeint(ref.MAPK_model, y0, t_long, args=(params_osc,))
MAPK_PP_osc = sol_osc[:, 4]


# Figure 8 재현해보기
plt.figure(figsize=(10, 9))
plt.plot(t_long / 60, MAPK_PP_osc, label=f'Ki={Ki_oscillation:.2f}')
plt.xlabel('Time (min)')
plt.ylabel('MAPK-PP Concentration (nM)')
plt.title('Figure 8')
plt.legend()
plt.grid(True)
plt.show()
