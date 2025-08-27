import networkx as nx
import random
import os
import copy
from pyboolnet import file_exchange
from pyboolnet.interaction_graphs import primes2igraph

def randomize_bnet_logic(original_bnet_path, new_bnet_filename="randomized_logic_network.bnet", rename_nodes=True):
    """
    Reads an existing .bnet file to extract its topology (nodes and edges).
    Then, it creates a new .bnet file with the identical topology,
    but with COMPLETELY RANDOM Boolean functions generated as COMPLEX expression strings
    based on each node's actual inputs from the original topology.
    Node names are typically renamed (Node1, Node2...) for clearer analysis of structural vs. functional impact.

    Args:
        original_bnet_path (str): Path to the original .bnet file.
        new_bnet_filename (str): Name for the new bnet file.
        rename_nodes (bool): If True, nodes are renamed to Node1, Node2... else original names. (RECOMMENDED TRUE for this type of randomization)
    Returns:
        str: Path to the newly created bnet file.
    """
    
    # 1. 원본 primes 로드 및 위상 구조 추출
    original_primes = file_exchange.bnet2primes(original_bnet_path)
    original_graph = primes2igraph(original_primes) 
    
    nodes_original_order = sorted(original_graph.nodes())
    
    # 2. 노드 이름 매핑 생성
    node_renaming_map = {}
    if rename_nodes:
        for i, original_name in enumerate(nodes_original_order):
            node_renaming_map[original_name] = f"Node{i+1}"
    else:
        node_renaming_map = {name: name for name in nodes_original_order}

    # 3. 새로운 .bnet 파일 내용 (텍스트 줄 리스트) 생성
    bnet_lines = []
    
    # ----------- 불리언 함수 생성 로직 - 이 부분을 대체합니다 -----------
    for original_node_name in nodes_original_order:
        new_node_name = node_renaming_map[original_node_name]
        
        predecessors_original = list(original_graph.predecessors(original_node_name))
        remapped_inputs_list = [node_renaming_map[pred] for pred in predecessors_original]

        function_expr_str = ""

        if not remapped_inputs_list: # 입력 노드가 없는 경우 -> 상수 노드
            function_expr_str = random.choice(['0','1'])
        else:
            # Stage 1: Create initial literals (NodeX or !NodeX)
            literals = []
            for inp in remapped_inputs_list:
                literals.append(f"!{inp}" if random.random() < 0.3 else inp)
            
            # If only one literal, that's the function
            if len(literals) == 1:
                function_expr_str = literals[0]
            else:
                # Stage 2: Combine literals into terms (random AND or OR)
                # Keep combining terms until one remains, or based on a complexity factor
                
                combined_terms_list = []
                
                # Decide how many sub-terms/literals to combine in one go (e.g., up to 3)
                max_sub_combine = min(len(literals), 3)
                
                current_processing_literals = list(literals) # Copy for manipulation

                # Iteratively combine literals/terms until complexity is built or few terms left
                while len(current_processing_literals) > 1 and random.random() < 0.8: # Probability to continue combining
                    num_to_combine = random.randint(2, min(len(current_processing_literals), max_sub_combine))
                    
                    # Randomly pick terms to combine
                    terms_to_combine_idx = random.sample(range(len(current_processing_literals)), num_to_combine)
                    terms_to_combine = [current_processing_literals[i] for i in sorted(terms_to_combine_idx, reverse=True)] # Pop in reverse order
                    for idx in sorted(terms_to_combine_idx, reverse=True):
                        current_processing_literals.pop(idx) # Remove from list
                        
                    inner_operator = " & " if random.random() < 0.6 else " | " # Favor AND for inner ops
                    combined_sub_term = f"({inner_operator.join(terms_to_combine)})"
                    
                    current_processing_literals.append(combined_sub_term) # Add combined term back
                
                # Final combination of remaining terms (if any) with a main operator
                if len(current_processing_literals) == 1:
                    function_expr_str = current_processing_literals[0]
                else:
                    outer_operator = " | " if random.random() < 0.7 else " & " # Favor OR for outer ops
                    function_expr_str = f"({outer_operator.join(current_processing_literals)})"

        # .bnet 파일의 한 줄을 만듦: "노드이름, 불리언_함수_표현식"
        bnet_lines.append(f"{new_node_name}, {function_expr_str}")
    # ----------- 불리언 함수 생성 로직 - 대체 끝 -----------

    # ... (나머지 코드 - .bnet 파일 직접 작성 및 검증 로직은 동일)
    output_path = os.path.join(os.getcwd(), new_bnet_filename)
    with open(output_path, "w") as f:
        for line in bnet_lines:
            f.write(line + "\n")

    print(f"Randomized logic Boolean network saved to: {output_path}")
    
    # ... (나머지 검증 코드는 이전과 동일)
    try:
        reloaded_primes = file_exchange.bnet2primes(output_path)
        reloaded_graph = primes2igraph(reloaded_primes)
        
        print(f"Verified Nodes: {reloaded_graph.number_of_nodes()}, Verified Edges: {reloaded_graph.number_of_edges()}")
        
        if original_graph.number_of_nodes() == reloaded_graph.number_of_nodes() and \
           original_graph.number_of_edges() == reloaded_graph.number_of_edges():
            print("Verification: Node and edge counts match the original network. Topology is perfectly preserved.")
        else:
            print("FATAL WARNING: Node or edge counts do NOT match the original network AFTER re-parsing! This indicates an issue with the randomly generated functions or PyBoolNet's parsing. Manual inspection is CRITICAL.")

    except Exception as e:
        print(f"Error during verification step: {e}. Manual check recommended.")

    return output_path

# --- 사용 예시 ---
emt_bnet_path = "./network/EMT_Network.bnet"

randomized_logic_bnet_path = randomize_bnet_logic(
    emt_bnet_path,
    new_bnet_filename="emt_randomized_logic_topology_preserved_complex_15.bnet",
    rename_nodes=True
)
"""
randomized_logic_bnet_path_no_rename = randomize_bnet_logic(
    emt_bnet_path,
    new_bnet_filename="emt_randomized_logic_topology_preserved_original_names.bnet",
    rename_nodes=False
)
"""
print("\nRandomized logic networks creation completed.")