import numpy as np
import networkx as nx
import itertools
import random
import matplotlib.pyplot as plt


# Weighted sum logic은 아직 하지 못함


state_transitions = {} # 각 초기조건의 다음 state를 dictionary 형태로 저장
stg = nx.DiGraph()

attractor_save = []
basin = {}



def make_initial_array(n):

    max_capacity = 14
    if n < max_capacity:
        all_initial_states = np.array(list(itertools.product([0, 1], repeat=n)))
    
    else:
        all_initial_states = np.zeros((10000, n), dtype=int)
        sampled_indices = random.sample(range(2**n), 10000)
            
        for i, idx in enumerate(sampled_indices):
            binary = format(idx, f'0{n}b')
            all_initial_states[i] = np.array([int(bit) for bit in binary])

    return all_initial_states


def update_state(n, network_logic, current_state):

    next_state = np.zeros(n, dtype=int)

    for i in range(n):
        logic = network_logic[i]
        for j in range(n):
            logic = logic.replace(f'x[{j}]', str(current_state[j]))
        
        next_state[i] = int(eval(logic))

    return next_state


def state_to_str(state):

    # [0, 0, 0]을 "000"으로 바꾸기
    return ''.join(map(str, state))

def str_to_state(state_str):

    # "000"을 [0, 0, 0]으로 바꾸기
    return np.array([int(bit) for bit in state_str])


def make_STG(n, network_logic):

    # STG 만들기

    # 1번 줄: N개의 노드를 가진 네트워크에 대하여 N by 𝟐^𝑵의 배열을 만들고,
    # 0과 1을 규칙적으로 채워 넣어 모든 초기조건을 포함한 배열을 제작 (용량 초과의 경우 무작위 샘플링)
    initial_states = make_initial_array(n)

    # 2번 줄: 각 초기조건의 다음 state를 dictionary 형태로 저장함
    for state in initial_states:
        state_str = state_to_str(state)
        next_state = update_state(n, network_logic, state)
        next_state_str = state_to_str(next_state)
        
        # 각 초기조건의 다음 state 저장, dictionary 형태로
        state_transitions[state_str] = next_state_str
        
        # STG에 node 및 edge 추가
        stg.add_node(state_str)
        stg.add_node(next_state_str)
        stg.add_edge(state_str, next_state_str)


def find_attractors():

    # 4번 줄: STG에서 cycle을 구성하는 노드를 모두 구함
    # networkx의 simple_cycles 함수 이용
    cycles = list(nx.simple_cycles(stg))
    
    # 크기가 1인 cycle은 fixed point attractor, 크기가 2 이상인 cycle은 cyclic attractor
    for cycle in cycles:
        if len(cycle) == 1:
            attractor_save.append(("point", cycle))
            attractor_key = f"point: {'->'.join(cycle)}"
        else:
            attractor_save.append(("cyclic", cycle))
            attractor_key = f"cyclic: {'->'.join(cycle)}"

        # attradtor_key를 가지고, basin dict를 만듦
        # basin은 일단 비어있는 list로 두기
        basin[attractor_key] = []


def find_basin():
    
    # 모든 노드에 대해 어떤 attractor에 도달할 수 있는지 확인
    for node in stg.nodes():
        for attractor_type, attractor in attractor_save:
            attractor_key = f"{attractor_type}: {'->'.join(attractor)}"
            try:
                # 노드에서 attractor의 첫 번째 노드로 가는 경로가 있는지 확인
                nx.shortest_path(stg, node, attractor[0])
                # 경로가 있으면 해당 attractor의 basin size 증가
                basin[attractor_key].append(node)
                # 하나의 attractor에 도달할 수 있으면 다음 노드로 넘어감
                break
            except:
                # 경로가 없으면 다음 attractor 확인
                pass


def draw_STG(save_path=None):

    plt.figure(figsize=(12, 12))
    
    # 노드 위치 계산
    pos = nx.spring_layout(stg, seed=42)
    
    # 일반 노드 그리기
    nx.draw_networkx_nodes(stg, pos, node_color='lightblue', node_size=10)
    
    # Attractor 노드 강조
    attractor_nodes = []
    for _, attractor in attractor_save:
        attractor_nodes.extend(attractor)
    
    nx.draw_networkx_nodes(stg, pos, nodelist=attractor_nodes, 
                            node_color='red', node_size=20)
    
    # 에지 그리기
    nx.draw_networkx_edges(stg, pos, arrows=True)
    
    # 노드 레이블 그리기
    nx.draw_networkx_labels(stg, pos, font_size=10)
    
    plt.title("State Transition Graph")
    plt.axis('off')
    
    if save_path:
        plt.savefig(save_path)
    
    plt.show()

def run_simulation(n, network_logic):

    # State Transition Graph 구축
    make_STG(n, network_logic)
    
    # Attractor 찾기
    find_attractors()
    
    # Basin 찾기
    find_basin()
    

def print_results():

    print(f"총 {len(attractor_save)}개의 attractor 발견")
    
    for i, (attractor_type, attractor) in enumerate(attractor_save):
        attractor_key = f"{attractor_type}: {'->'.join(attractor)}"
        basins = basin.get(attractor_key, 0)
        basin_size = len(basins)
        
        if attractor_type == "fixed_point":
            state_array = str_to_state(attractor[0])
            print(f"\nPoint Attractor {i+1} (Basin Size: {basin_size}):")
            print(f"  State: {attractor[0]} = {state_array}")
            print(f"basins: {basins}")
        else:
            print(f"\nCyclic Attractor {i+1} (길이: {len(attractor)}, Basin Size: {basin_size}):")
            for state_str in attractor:
                state_array = str_to_state(state_str)
                print(f"  State: {state_str} = {state_array}")
            print(f"basins: {basins}")


# A*= A and not C
# B*= A or C
# C*= not B
network_logic_1 = [
    'x[0] and not x[2]',
    'x[0] or x[2]',
    'not x[1]'
]


# n1*= n2
# n2*= ( n1 or n3 ) and n4
# n3*= not n2
# n4*= n5
# n5*= n4
network_logic_2 = [
    'x[2]',
    '( x[0] or x[2] ) and x[3]',
    'not x[1]',
    'x[4]',
    'x[3]'
]

run_simulation(5, network_logic_2)
print_results()
draw_STG()
