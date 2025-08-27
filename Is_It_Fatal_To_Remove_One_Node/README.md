# Is It Fatal To Remove One Onde
+ 생물학적 네트워크를 만들 때, Literature-based Modeling 과정에서 노드 하나를 까먹고 넣지 않으면 얼마나 Fatal할까?  
+ 이 코드는 A Cell-Fate Reprogramming Strategy Reverses Epithelial-to-Mesenchymal Transition of Lung Cancer Cells While Avoiding Hybrid States 논문을 이용한 BSiE 여름방학 개별연구 결과입니다.  

**Reference paper:**  A Cell-Fate Reprogramming Strategy Reverses Epithelial-to-Mesenchymal Transition of Lung Cancer Cells While Avoiding Hybrid States
https://doi.org/10.1158/0008-5472.CAN-22-1559

## Requirements

+ 이 코드는 Python 3.9.x에서 만들었습니다. Anaconda 가상환경을 이용하였습니다.  
+ pyboolnet: <https://github.com/hklarner/pyboolnet> 이 설치되어야 합니다.
+ jupyter notebook을 이용해 실행할 수 있습니다.


## Implementation

+ Import networks in BoolNet format (from the `network` directory)  
+ A simple toy network example is provided.  

+ 1.(...).ipynb : 기존 논문을 재현하는 데 사용할 수 있는 코드입니다. Single Node Perturbation을 수행할 수 있습니다.  
+ 2.(...).ipynb : 노드 하나를 없애고, 해당 노드의 로직만 보존했을 때 Attractor Landscape가 어떻게 되는지에 대한 실험 코드입니다. 기존 Original Network와 Attractor가 동일한지 자동으로 비교해줍니다. 


## Notes

+ 주요 함수들은 'modules' 폴더 안에 있습니다.
+ 사용된 Network 파일은 'network' 폴더 안에 있습니다.
+ make_graph.py : bnet 파일을 이용해 그래프를 pdf 파일 형태로 만들어줍니다.
+ make_rn_using_EMT.py : EMT_Network 파일을 이용해 Random Network를 만들어줍니다. (EMT_Network와 같은 수의 Node와 Edge를 맞추기 위해서)
