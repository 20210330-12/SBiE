# -*- coding: utf-8 -*-
"""
네트워크 attractor 및 basin size 계산 프로그램
출력: 각 attractor와 해당 basin size 출력
"""

import random

# ------------------------------
# Step 1. Define Inputs and Settings
# ------------------------------
N = 6  # 네트워크의 노드 개수 (원하는 크기로 수정 가능)
total_initial_states = 2**N  # 가능한 총 초기 상태

# 전체 상태 공간이 너무 클 경우를 대비해 샘플링 여부 결정
CAPACITY_THRESHOLD = 2**10  # 임계값 (예: 2^10 보다 작으면 전체 생성, 크면 샘플링)
USE_RANDOM_SAMPLING = total_initial_states > CAPACITY_THRESHOLD
SAMPLE_SIZE = 50  # 샘플링할 경우 사용할 초기 상태 개수 (원하는 크기로 수정 가능)

# 네트워크 로직 정의 (여기서는 단순히 비트를 반전시키는 예제)
# replace와 eval을 사용하여 old_state 에 기반한 next_state를 생성
# network_logic_str 에서 "old_state" 문자열을 그대로 사용함.
network_logic_str = "next_state = [s ^ 1 for s in old_state]"

# ------------------------------
# Step 2. Generate Initial Conditions Array
# ------------------------------
def generate_all_initial_conditions(n):
    """
    모든 초기 조건(이진 상태)을 생성 (풀 생성)
    """
    initial_states = []
    total = 2**n
    for i in range(total):
        # 이진수 형태의 문자열을 N 길이에 맞게 0으로 채움
        bin_str = format(i, '0{}b'.format(n))
        state = [int(ch) for ch in bin_str]
        initial_states.append(state)
    return initial_states

def generate_random_initial_conditions(n, sample_size):
    """
    sample_size 개수만큼 무작위 이진 상태 생성
    """
    initial_states = []
    for _ in range(sample_size):
        state = [random.randint(0, 1) for _ in range(n)]
        initial_states.append(state)
    return initial_states

if USE_RANDOM_SAMPLING:
    initial_conditions = generate_random_initial_conditions(N, SAMPLE_SIZE)
else:
    initial_conditions = generate_all_initial_conditions(N)

# ------------------------------
# Step 3. Define network update function using eval
# ------------------------------
def update_state(old_state):
    """
    network_logic_str을 이용하여 old_state에 대한 next_state 계산
    replace 및 eval 사용 -> 안전한 환경 제공을 위해 별도의 dictionary 사용
    """
    # 로직 문자열 준비. 여기서는 별도의 변환은 없으므로 그대로 사용.
    logic_str = network_logic_str
    # eval 실행: 전역 네임스페이스 대신 제한된 로컬 네임스페이스 사용
    local_dict = {'old_state': old_state}
    exec(logic_str, {}, local_dict)  # exec로 network_logic_str 실행
    next_state = local_dict['next_state']
    # 결과가 올바른 길이인지 확인
    if len(next_state) != len(old_state):
        raise ValueError("네트워크 업데이트 결과 상태 길이가 올바르지 않습니다.")
    return next_state

# ------------------------------
# Step 4. Process Each Initial Condition
# ------------------------------
# attractors_storage: 고유 attractor의 서명(튜플 형태) 리스트
# basin_sizes: attractor 서명을 key로 하여 basin size를 저장하는 딕셔너리
attractors_storage = {}
# 각 초기 상태마다 attractor를 찾으면서 진행
for init_state in initial_conditions:
    # 3.1. 임시 배열(temp_state) 초기화
    temp_state = init_state.copy()
    # 3.2. trajectory 저장공간 초기화 (처음 상태 저장)
    trajectory = [tuple(temp_state)]  # 리스트를 튜플로 저장하여 불변으로 사용

    while True:
        # 4.a. network_logic을 사용해 다음 상태 계산
        next_state = update_state(list(temp_state))
        next_state_tuple = tuple(next_state)
        # 4.b. trajectory에 이미 존재하는지 확인
        if next_state_tuple in trajectory:
            # attractor에 도달하면, 사이클 추출 (처음 반복 상태부터 끝까지)
            first_index = trajectory.index(next_state_tuple)
            attractor = tuple(trajectory[first_index:])  # attractor는 튜플의 튜플
            break
        else:
            # 새로운 상태이면, trajectory에 추가하고 temp_state 업데이트
            trajectory.append(next_state_tuple)
            temp_state = next_state

    # ------------------------------
    # Step 5. Record Attractor and Basin Size
    # ------------------------------
    # attractor을 문자열 형태 또는 튜플 형태로 저장하여 고유성 체크
    if attractor in attractors_storage:
        attractors_storage[attractor] += 1  # basin size +1
    else:
        attractors_storage[attractor] = 1    # 새로운 attractor, 초기 basin size 1

# ------------------------------
# Step 6. Final Output and Summary
# ------------------------------
# attractors와 그 basin size를 출력
print("발견된 attractor와 해당 basin size:")
for attr, basin in attractors_storage.items():
    # attractor를 보기 쉽게 변환하여 출력
    print("Attractor:", attr, "-> Basin Size:", basin)

"""
프로그램 동작에 대한 단계별 설명 (한국어):

1. 입력 및 설정:
   - 네트워크의 노드 개수 N을 설정하고, 가능한 초기 조건 개수 (2^N)를 구합니다.
   - 전체 초기 조건 상태가 너무 많을 경우를 대비하여, 임계값을 정해 샘플링할 것인지 전체 생성할 것인지를 결정합니다.
   - 여기서는 단순한 네트워크 로직을 "next_state = [s ^ 1 for s in old_state]"로 정의하여 모든 비트를 반전시키도록 하였습니다.

2. 초기 조건 배열 생성:
   - 만약 전체 상태 공간이 임계값 이하이면, 0부터 (2^N - 1)까지 모든 정수를 이진수 문자열로 변환하여 초기 조건 배열을 만듭니다.
   - 임계값을 초과하는 경우, SAMPLE_SIZE 만큼의 무작위 상태를 생성합니다.

3. 네트워크 업데이트 함수:
   - update_state 함수는 현재 상태(old_state)를 입력받아, 정의된 network_logic_str을 exec와 eval을 사용하여 다음 상태(next_state)를 구합니다.
   - 계산된 next_state의 길이가 입력 상태와 동일한지 확인합니다.

4. 각 초기 조건에 대해 시뮬레이션:
   - 각 초기 조건을 시작으로, temp_state와 trajectory 저장공간(튜플 형태로 상태 저장)을 초기화합니다.
   - while 루프 내에서 update_state 함수를 통해 다음 상태를 계산하고, 해당 상태가 trajectory에 이미 존재하는지 확인합니다.
   - 이미 존재한다면, 첫 번째 등장 위치부터 사이클( attractor )을 추출하고 루프를 종료합니다.
   - 그렇지 않으면, 새로운 상태를 trajectory에 추가하고 업데이트된 temp_state로 진행합니다.

5. attractor 정보 및 basin size 기록:
   - 찾은 attractor을 고유 서명(튜플의 튜플 형태)으로 저장하고, 만약 이미 저장된 attractor이라면 그 basin size를 1 증가시키며, 처음 발견된 attractor라면 basin size를 1로 초기화합니다.

6. 최종 출력:
   - 모든 초기 조건 처리 후, 발견된 각 attractor과 해당하는 basin size를 출력합니다.
"""
