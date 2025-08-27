# --------------- 로직 변경 확인 함수 ---------------
from pyboolnet import file_exchange # primes 구조를 시각적으로 보여주는 데 유용

def print_node_logic(node_name, primes_obj):
    """
    primes 객체에서 특정 노드의 Boolean function을 출력합니다.
    """
    if node_name not in primes_obj:
        print(f"경고: 노드 '{node_name}'은 primes 객체에 존재하지 않습니다.")
        return

    node_prime = primes_obj[node_name]

    print(f"\n--- 노드 '{node_name}'의 Boolean Function ---")
    if isinstance(node_prime, list) and len(node_prime) == 2:
        inputs = node_prime[0]
        truth_table = node_prime[1]

        print(f"  입력 노드들: {inputs if inputs else '없음 (상수)'}")
        print(f"  진리표 (Truth Table): {truth_table}")

        # 로직이 '제거'되었는지 (즉, 상수 함수인지) 판단
        if not inputs and isinstance(truth_table, dict) and len(truth_table) == 1 and () in truth_table:
            constant_value = truth_table[()]
            print(f"  ==> 확인: 이 노드는 입력에 무관하게 항상 '{constant_value}'을(를) 출력하는 상수 함수입니다 (로직 제거됨).")
        else:
            print("  ==> 확인: 이 노드는 여전히 입력에 의존하는 복잡한 로직을 가지고 있습니다.")

    elif isinstance(node_prime, dict) and 'inputs' in node_prime and 'function' in node_prime:
        # PyBoolNet 3.x의 다른 primes 표현 방식일 경우
        print(f"  (Dict 형식) 입력 노드들: {node_prime['inputs']}")
        print(f"  (Dict 형식) 함수: {node_prime['function']}")
        if not node_prime['inputs'] and isinstance(node_prime['function'], dict) and len(node_prime['function']) == 1 and () in node_prime['function']:
            constant_value = node_prime['function'][()]
            print(f"  ==> 확인: 이 노드는 입력에 무관하게 항상 '{constant_value}'을(를) 출력하는 상수 함수입니다 (로직 제거됨).")
        else:
            print("  ==> 확인: 이 노드는 여전히 입력에 의존하는 복잡한 로직을 가지고 있습니다.")
    else:
        print(f"  알 수 없는 primes 형식: {type(node_prime)}")