import networkx as nx
from pyboolnet import file_exchange
from pyboolnet.interaction_graphs import primes2igraph
# from pyboolnet.state_transition_graphs import stgs # <-- 이 줄 삭제!
import pyboolnet.state_transition_graphs as sts_graphs # <-- 이렇게 임포트!

def visualize_network_structure(bnet_file, output_pdf):
    # 1. .bnet 파일 로드
    primes = file_exchange.bnet2primes(bnet_file)
    # 2. 그래프 생성
    graph = primes2igraph(primes)

    # 3. NetworkX DiGraph 생성 및 라벨링 (PyBoolNet이 기본 제공하는 DiGraph 사용도 가능)
    G = nx.DiGraph()
    # 노드를 추가할 때 label 속성도 추가 (graphviz에서 노드에 텍스트 표시용)
    for node in graph.nodes():
        G.add_node(node, label=node) # node 이름으로 label 설정
    # 엣지 추가
    for u, v in graph.edges():
        G.add_edge(u, v)

    # 4. pyboolnet의 sts_graphs.digraph2image 함수로 pdf 생성 (graphviz 필요)
    # layout_engine은 "dot"이 가장 일반적
    sts_graphs.digraph2image(G, output_pdf, layout_engine="dot")
    print(f"네트워크 구조 시각화 결과가 {output_pdf} 파일로 저장되었습니다.")

# 사용 예시 (이 부분은 이전과 동일)
#bnet_path = "./emt_randomized_logic_topology_preserved_original_names.bnet"  # 네가 원하는 .bnet 파일 경로
bnet_path = "emt_randomized_logic_topology_preserved_complex.bnet"
#output_pdf_path = "./emt_randomized_logic_topology_structure.pdf"
output_pdf_path = "./Random_Network_structure.pdf"

visualize_network_structure(bnet_path, output_pdf_path)

print("\nRandomized logic networks creation completed. Check generated PDF files.") # 이 부분은 전체 실행용이면 한번만