import numpy as np
import random
import itertools

class BooleanNetworkSimulation:
    def __init__(self, network_logic, num_nodes, max_samples=None):
        """
        초기화 함수
        
        Parameters:
        -----------
        network_logic : list of str
            각 노드의 상태 전이 로직을 담은 리스트
            예: ['x[1] and not x[2]', 'x[0] or x[2]', 'not x[0]']
        num_nodes : int
            네트워크의 노드 개수
        max_samples : int, optional
            초기조건 샘플링 개수 (None이면 모든 초기조건 사용)
        """
        self.network_logic = network_logic
        self.num_nodes = num_nodes
        self.max_samples = max_samples
        self.attractors = []
        self.basin_sizes = []
        
    def generate_initial_states(self):
        """
        모든 가능한 초기 상태를 생성하거나 샘플링
        
        Returns:
        --------
        numpy.ndarray
            초기 상태 배열 (shape: num_states x num_nodes)
        """
        # 총 가능한 상태 수 계산
        total_states = 2**self.num_nodes
        
        # 초기 상태 배열 생성
        if self.max_samples is None or self.max_samples >= total_states:
            # 모든 가능한 초기 상태 생성
            all_states = np.array(list(itertools.product([0, 1], repeat=self.num_nodes)))
            print(all_states)
        else:
            # 무작위 샘플링
            all_states = np.zeros((self.max_samples, self.num_nodes), dtype=int)
            sampled_indices = random.sample(range(total_states), self.max_samples)
            
            for i, idx in enumerate(sampled_indices):
                # idx를 이진수로 변환하여 상태 설정
                binary = format(idx, f'0{self.num_nodes}b')
                all_states[i] = np.array([int(bit) for bit in binary])
                
        return all_states
    
    def update_state(self, state):
        """
        현재 상태에서 다음 상태로 업데이트
        
        Parameters:
        -----------
        state : numpy.ndarray
            현재 상태 (shape: num_nodes)
        
        Returns:
        --------
        numpy.ndarray
            다음 상태 (shape: num_nodes)
        """
        next_state = np.zeros(self.num_nodes, dtype=int)
        print(f"현재 state: {state}")
        # 각 노드의 다음 상태 계산
        for i in range(self.num_nodes):
            # 로직 문자열에서 x[j]를 state[j]로 치환
            logic = self.network_logic[i]
            for j in range(self.num_nodes):
                logic = logic.replace(f'x[{j}]', str(state[j]))
            
            # 로직 평가
            next_state[i] = int(eval(logic))
            # print(f"{i}번째: {logic}")

        print(f"다음 state: {next_state}")
        return next_state
    
    def find_attractor(self, initial_state):
        """
        초기 상태에서 시작하여 attractor 찾기
        
        Parameters:
        -----------
        initial_state : numpy.ndarray
            초기 상태 (shape: num_nodes)
        
        Returns:
        --------
        list
            attractor의 상태들 (리스트 내 각 요소는 numpy.ndarray)
        """
        trajectory = [initial_state.copy()]
        current_state = initial_state.copy()
        print(f"trajectory: {trajectory}")
        print(f"current state: {current_state}")
        
        while True:
            next_state = self.update_state(current_state)
            print(f"next_state: {next_state}")
            # trajectory에서 현재 상태의 인덱스 찾기
            for i, state in enumerate(trajectory):
                if np.array_equal(next_state, state):
                    # attractor 발견
                    print(f"attractor 발견: {trajectory[i:]}")
                    return trajectory[i:]
            
            # 새로운 상태 추가
            trajectory.append(next_state.copy())
            current_state = next_state.copy()
    
    def run_simulation(self):
        """
        Boolean Network Simulation 실행
        
        Returns:
        --------
        tuple
            (attractors, basin_sizes)
            attractors: 발견된 모든 attractor 리스트
            basin_sizes: 각 attractor의 basin size 리스트
        """
        initial_states = self.generate_initial_states()

        print(f"첫 state: {initial_states}")
        
        for initial_state in initial_states:
            attractor = self.find_attractor(initial_state)
            
            # attractor를 튜플 형태로 변환 (해시 가능하게)
            attractor_tuple = tuple(map(tuple, attractor))
            
            # 이미 발견된 attractor인지 확인
            found = False
            for i, existing_attractor in enumerate(self.attractors):
                existing_tuple = tuple(map(tuple, existing_attractor))
                if existing_tuple == attractor_tuple:
                    self.basin_sizes[i] += 1
                    found = True
                    break
            
            # 새로운 attractor인 경우 추가
            if not found:
                self.attractors.append(attractor)
                self.basin_sizes.append(1)
        
            print(f"attractors: {self.attractors}")
            print(f"basin size: {self.basin_sizes}")

        return self.attractors, self.basin_sizes
    
    def print_results(self):
        """
        시뮬레이션 결과 출력
        """
        print(f"총 {len(self.attractors)}개의 attractor를 발견했습니다.")
        
        for i, attractor in enumerate(self.attractors):
            print(f"\nAttractor {i+1} (Basin Size: {self.basin_sizes[i]}):")
            if len(attractor) == 1:
                print(f"  Point attractor: {attractor[0]}")
            else:
                print(f"  Cycle attractor (길이: {len(attractor)}):")
                for state in attractor:
                    print(f"    {state}")

# 사용 예시
if __name__ == "__main__":
    # 예시 네트워크 로직 (3 노드 네트워크)
    # 노드 1: 노드 2가 0이고 노드 3이 1이면 1, 아니면 0
    # 노드 2: 노드 1이 1이면 1, 아니면 0
    # 노드 3: 노드 1이 0이면 1, 아니면 0
    # network_logic = [
    #     'x[1] == 0 and x[2] == 1',
    #     'x[0] == 1',
    #     'x[0] == 0'
    # ]

    network_logic = [
    'x[0] and not x[2]',  # A*= A and not C
    'x[0] or x[2]',       # B*= A or C
    'not x[1]'            # C*= not B
    ]
    
    # 시뮬레이션 실행
    sim = BooleanNetworkSimulation(network_logic, num_nodes=3)
    sim.run_simulation()
    sim.print_results()
