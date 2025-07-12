import numpy as np
import networkx as nx
import itertools
import random
import matplotlib.pyplot as plt
from collections import defaultdict



network_logic = network_logic
num_nodes = num_nodes
max_samples = max_samples
state_transitions = {}  # Dictionary to store state transitions
stg = nx.DiGraph()      # State Transition Graph
attractors = []         # List to store attractors
basin_sizes = {}        # Dictionary to store basin sizes
    
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


def state_to_str(self, state):
    """
    상태 배열을 문자열로 변환
    
    Parameters:
    -----------
    state : numpy.ndarray
        상태 배열
        
    Returns:
    --------
    str
        상태를 나타내는 문자열 (예: '101')
    """
    return ''.join(map(str, state))

def str_to_state(self, state_str):
    """
    문자열을 상태 배열로 변환
    
    Parameters:
    -----------
    state_str : str
        상태를 나타내는 문자열 (예: '101')
        
    Returns:
    --------
    numpy.ndarray
        상태 배열
    """
    return np.array([int(bit) for bit in state_str])

def build_state_transition_graph(self):
    """
    State Transition Graph 구축
    """
    # 초기 상태 생성
    initial_states = self.generate_initial_states()
    
    # 모든 초기 상태에 대해 다음 상태 계산 및 그래프에 추가
    for state in initial_states:
        state_str = self.state_to_str(state)
        next_state = self.update_state(state)
        next_state_str = self.state_to_str(next_state)
        
        # 상태 전이 저장
        self.state_transitions[state_str] = next_state_str
        
        # 그래프에 노드 및 에지 추가
        self.stg.add_node(state_str)
        self.stg.add_node(next_state_str)
        self.stg.add_edge(state_str, next_state_str)

def find_attractors(self):
    """
    STG에서 attractor 찾기
    """
    # NetworkX의 simple_cycles 함수를 사용하여 모든 cycle 찾기
    cycles = list(nx.simple_cycles(self.stg))
    
    # 크기 1인 cycle은 fixed point, 크기 2 이상인 cycle은 cyclic attractor
    for cycle in cycles:
        if len(cycle) == 1:
            # 자기 자신을 가리키는 루프가 있는지 확인
            if self.stg.has_edge(cycle[0], cycle[0]):
                self.attractors.append(("fixed_point", [cycle[0]]))
        else:
            self.attractors.append(("cyclic", cycle))

def calculate_basin_sizes(self):
    """
    각 attractor의 basin size 계산
    """
    # 각 attractor에 대한 basin 크기 초기화
    for attractor_type, attractor in self.attractors:
        attractor_key = f"{attractor_type}:{'->'.join(attractor)}"
        self.basin_sizes[attractor_key] = 0
    
    # 모든 노드에 대해 어떤 attractor에 도달할 수 있는지 확인
    for node in self.stg.nodes():
        for attractor_type, attractor in self.attractors:
            attractor_key = f"{attractor_type}:{'->'.join(attractor)}"
            try:
                # 노드에서 attractor의 첫 번째 노드로 가는 경로가 있는지 확인
                path = nx.shortest_path(self.stg, node, attractor[0])
                # 경로가 있으면 해당 attractor의 basin size 증가
                self.basin_sizes[attractor_key] += 1
                # 하나의 attractor에 도달할 수 있으면 다음 노드로 넘어감
                break
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                # 경로가 없으면 다음 attractor 확인
                continue

def plot_state_transition_graph(self, save_path=None):
    """
    State Transition Graph 시각화
    
    Parameters:
    -----------
    save_path : str, optional
        그래프 이미지 저장 경로
    """
    plt.figure(figsize=(12, 12))
    
    # 노드 위치 계산
    pos = nx.spring_layout(self.stg, seed=42)
    
    # 일반 노드 그리기
    nx.draw_networkx_nodes(self.stg, pos, node_color='lightblue', node_size=500)
    
    # Attractor 노드 강조
    attractor_nodes = []
    for _, attractor in self.attractors:
        attractor_nodes.extend(attractor)
    
    nx.draw_networkx_nodes(self.stg, pos, nodelist=attractor_nodes, 
                            node_color='red', node_size=700)
    
    # 에지 그리기
    nx.draw_networkx_edges(self.stg, pos, arrows=True)
    
    # 노드 레이블 그리기
    nx.draw_networkx_labels(self.stg, pos, font_size=10)
    
    plt.title("State Transition Graph")
    plt.axis('off')
    
    if save_path:
        plt.savefig(save_path)
    
    plt.show()

def run_simulation(self):
    """
    Boolean Network Simulation 실행
    
    Returns:
    --------
    tuple
        (attractors, basin_sizes)
    """
    # State Transition Graph 구축
    self.build_state_transition_graph()
    
    # Attractor 찾기
    self.find_attractors()
    
    # Basin size 계산
    self.calculate_basin_sizes()
    
    return self.attractors, self.basin_sizes

def print_results(self):
    """
    시뮬레이션 결과 출력
    """
    print(f"총 {len(self.attractors)}개의 attractor를 발견했습니다.")
    
    for i, (attractor_type, attractor) in enumerate(self.attractors):
        attractor_key = f"{attractor_type}:{'->'.join(attractor)}"
        basin_size = self.basin_sizes.get(attractor_key, 0)
        
        if attractor_type == "fixed_point":
            state_array = self.str_to_state(attractor[0])
            print(f"\nFixed Point Attractor {i+1} (Basin Size: {basin_size}):")
            print(f"  State: {attractor[0]} = {state_array}")
        else:
            print(f"\nCyclic Attractor {i+1} (길이: {len(attractor)}, Basin Size: {basin_size}):")
            for state_str in attractor:
                state_array = self.str_to_state(state_str)
                print(f"  State: {state_str} = {state_array}")

# 사용 예시
if __name__ == "__main__":
    # A*= A and not C
    # B*= A or C
    # C*= not B
    network_logic = [
        'x[0] and not x[2]',  # A*= A and not C
        'x[0] or x[2]',       # B*= A or C
        'not x[1]'            # C*= not B
    ]
    
    # 시뮬레이션 실행
    sim = BooleanNetworkSimulation(network_logic, num_nodes=3)
    sim.run_simulation()
    sim.print_results()
    
    # State Transition Graph 시각화
    sim.plot_state_transition_graph()
