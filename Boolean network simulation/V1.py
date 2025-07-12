import numpy as np
import random
import itertools

# 이 코드에서의 문제점!! 같은 attractor을 구분해내지 못한다

# [0 0 0]
# [0 0 1]
# [0 1 1]
# [0 1 0] 과

# [0 1 0]
# [0 0 0]
# [0 0 1]
# [0 1 1] 은 같은 attractor 인데...

def make_initial_array(n):

    # 용량 = 4라고 해보자
    max_capacity = 4
    if n < max_capacity:
        # 모든 가능한 초기 상태
        all_initial_states = np.array(list(itertools.product([0, 1], repeat=n)))
    
    else:
        # 용량 초과의 경우 무작위 샘플링
        # 최대 10개의 초기 상태만 쓴다고 가정
        all_initial_states = np.zeros((10, n), dtype=int)
        sampled_indices = random.sample(range(2**n), 10)
            
        for i, idx in enumerate(sampled_indices):
            # idx를 이진수로 변환하여 상태 설정
            binary = format(idx, f'0{n}b')
            all_initial_states[i] = np.array([int(bit) for bit in binary])

    return all_initial_states


def update_state(n, network_logic, current_state):

    # 4번 줄: replace, eval 함수를 이용해서,
    # 네트워크 로직에 임시배열, 여기서는 current_state를 넣고
    # 다음 상태, 여기서는 next_state 노드값 배열을 구함

    next_state = np.zeros(n, dtype=int)

    # 각 노드의 다음 상태 계산
    for i in range(n):
        # 로직 문자열에서, 문자로 되어있는 걸 숫자로 치환
        logic = network_logic[i]
        for j in range(n):
            logic = logic.replace(f'x[{j}]', str(current_state[j]))
        
        # 로직 평가
        next_state[i] = int(eval(logic))

    return next_state


def find_attractor(n, network_logic, initial_state):

    # 2번 줄: 제작한 배열을 한 줄 읽어와 임시배열로 사용
    # 여기서 한 줄은 initial_state로 이미 받음
    tmp_array = initial_state.copy()
    # 3번 줄: Trajectory라는 저장공간, 그 첫칸에 한 줄의 임시배열을 저장
    trajectory = [initial_state.copy()]
    
    while True:
        # 4번 줄: 네트워크 로직에 임시배열을 넣고 다음 상태의 노드값 배열을 구함
        next_state = update_state(n, network_logic, tmp_array)

        # 5번 줄: 얻어진 노드값 배열이 trajectory 저장공간 내에 이미 존재하는지 비교
        for i, state in enumerate(trajectory):
            if np.array_equal(next_state, state):
                # 6번 줄: 이미 존재함 -> attractor로 분류
                return trajectory[i:]
        
        # 6번 줄: trajectory array를 모두 돌렸는데도 없다면,
        # 임시배열에 덮어씌우고,
        # trajectory의 다음 공간에 저장, 즉 append 하고,
        # 다시 4번 줄로 (while True 구문이라 계속 update_state 함수 수행할 것)
        trajectory.append(next_state.copy())
        tmp_array = next_state.copy()


def run_simulation(n, network_logic):

    # 1번 줄: N개의 노드를 가진 네트워크에 대하여 N by 𝟐^𝑵의 배열을 만들고,
    # 0과 1을 규칙적으로 채워 넣어 모든 초기조건을 포함한 배열을 제작 (용량 초과의 경우 무작위 샘플링)
    initial_states = make_initial_array(n)

    # 7번 줄: Attractor 저장공간 및 basin size 저장배열을 만들고,
    attractor_save = []
    basin_sizes = []
    
    # 10번 줄: 모든 초기 조건에 대하여 반복
    # 2번 줄: 제작한 배열을 한 줄 읽어와 임시배열로 사용
    for initial_state in initial_states:

        attractor = find_attractor(n, network_logic, initial_state)
        
        # attractor를 튜플 형태로 변환 (해시 가능하게)
        attractor_tuple = tuple(map(tuple, attractor))
        
        # 8번 줄: 다음 attractor가 구해지면,
        # 해당 attractor가 이미 attractor 저장공간에 존재하는지 확인
        found = False
        for i, existing_attractor in enumerate(attractor_save):
            existing_tuple = tuple(map(tuple, existing_attractor))
            if existing_tuple == attractor_tuple:
                # 9번 줄: 이미 존재한다면 해당 attractor의 basin size 저장배열 값을 +1
                basin_sizes[i] += 1
                found = True
                break
        
        # 9번 줄: 존재하지 않는다면 다음 attractor 저장공간에 저장
        # basin size 저장배열에 1을 입력 후 2번 줄로
        if not found:
            attractor_save.append(attractor)
            basin_sizes.append(1)


    return attractor_save, basin_sizes





now_logic = [
    'x[0] and not x[2]',  # A*= A and not C
    'x[0] or x[2]',       # B*= A or C
    'not x[1]'            # C*= not B
]

attractor_save, basin_sizes = run_simulation(3, now_logic)



print(f"총 {len(attractor_save)}개의 attractor 발견")

for i, attractor in enumerate(attractor_save):
    print(f"\nAttractor {i+1} (Basin Size: {basin_sizes[i]}):")
    if len(attractor) == 1:
        print(f"  Point attractor: {attractor[0]}")
    else:
        print(f"  Cycle attractor (길이: {len(attractor)}):")
        for state in attractor:
            print(f"    {state}")