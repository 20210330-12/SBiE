# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 15:25:04 2020

@ author: Namhee Kim
@ We used a python package ‘PyBoolNet’ for attractor simulation (https://github.com/hklarner/pyboolnet)

"""



import os
import time
import pandas as pd
import numpy as np
from collections import defaultdict
import networkx as nx
from typing import List, Dict
import random

from pyboolnet.prime_implicants import create_constants
from pyboolnet.state_transition_graphs import primes2stg

my_env = os.environ.copy()
my_env["PATH"]
Vector1 = Dict[str, str]
Vector2 = List[str]   


#===========================================================
# Random sampling
#===========================================================
def rand_initial_states(num_of_state, num_of_nodes):
    """
    # generate random Boolean initial states
    
    Parameters
    ----------
    num_of_state : int
    num_of_nodes : int     
    """
    if (num_of_nodes <= 32) | (num_of_state*10000 > (2**num_of_nodes)) :     
        rand_int = random.sample(range(2**num_of_nodes), num_of_state)
    else :
        range_num = num_of_state*100000
        rand_int = random.sample(range(range_num), num_of_state)
        print("WARNING : Out of memory!")
        
    s = [bin(x)[2:] for x in list(rand_int)]
    initset = [('0'*(num_of_nodes-len(x))+x) for x in list(s)]   

    return initset

#===========================================================
# Basins of attraction
#===========================================================
def compute_attractor_from_primes(primes, update_mode, initState):
    """
    # compute basin sizes from stg computed by (@pyboolnet)
    # using pyboolnet.state_transition_graphs.primes2stg
    
    Parameters
    ----------
    primes : primes (@pyboolnet)
    update_mode : str ('synchronous' or 'asynchronous')
    initState : List (random sampling)
    """
    stg = primes2stg(primes, update_mode, initState)
    
    attrs_fromSTG = defaultdict()
    for idx, att in enumerate(nx.simple_cycles(stg)):
        attrs_fromSTG[idx] = defaultdict()
        attrs_fromSTG[idx]['attractors'] = tuple(str(x) for x in att)
        attrs_fromSTG[idx]['basinsizes'] = 0
        
        for node in stg.nodes:
            try:
                nx.shortest_path(stg, node, att[0])
                attrs_fromSTG[idx]['basinsizes'] += 1
            except: # there is no path
                continue
            
        attrs_fromSTG[idx]['perc'] = attrs_fromSTG[idx]['basinsizes'] / len(stg.nodes())
    return attrs_fromSTG


#===========================================================
# Phenotype
#===========================================================
def define_phenotype_from_att(primes, phenotype:Vector1, phenotypeAnnot:Vector1, att):
    nodeList = list(primes.keys())
    att_mean = np.mean(att,axis=0)
    annot = 10
    for name, marker in phenotype.items():
        if np.prod([np.rint(np.nextafter((att_mean[nodeList.index(m)]),(att_mean[nodeList.index(m)])+1)) == bool(marker[m]) for m in marker.keys()]) == 1:
            annot = phenotypeAnnot[name]
    return annot

def str2array(x):
    if type(x) == str: # np.str 대신 str로 변경
        array = np.array([[int(y) for y in x]])
    else:
        array = np.zeros((len(x),len(x[0])))
        for idx, x0 in enumerate(x):
            array[idx,:] = np.array([int(x) for x in x0])
    return array
    
def compute_phenotype(primes, attrs_fromSTG, phenotype, phenotypeAnnot):
    """
    # determine phenotype of an attractor 

    Parameters
    ----------    
    primes : primes (@pyboolnet)
    attrs_fromSTG : the output of 'compute_attractor_from_primes'
    phenotype : Dict ({phenotype:phenotype markers})
    phenotypeAnnot : Dict (simple annotation of phenotype)
    """    
    for idx in range(len(attrs_fromSTG)):
        att = str2array(attrs_fromSTG[idx]['attractors'])
        attrs_fromSTG[idx]['phenotype'] = define_phenotype_from_att(primes, phenotype, phenotypeAnnot, att)

    return attrs_fromSTG



#===========================================================
# Attractor simulation
#===========================================================
def makePhenotypeDF(attrs_dict, phenotypeAnnot):
    df = pd.DataFrame({'phenotype':[[pheno for pheno, phenoIdx in phenotypeAnnot.items() if phenoIdx == x][0] for x in [x['phenotype'] for x in attrs_dict.values()]],
                                     'Ratio':[x['perc'] for x in attrs_dict.values()]})
    pheno_df = df.groupby('phenotype').sum()
    return(pheno_df)

def Simulation(constantDict, primes, update_mode, initState, phenotype, phenotypeAnnot):
    """
    # compute average node activites based on basin sizes
    
    Parameters
    ----------
    constantDict : Dict
    primes : primes (@pyboolnet)
    update_mode : str ('synchronous' or 'asynchronous')
    initState : List (random sampling)
    phenotype : Dict ({phenotype:phenotype markers})
    phenotypeAnnot : Dict (simple annotation of phenotype)
    """
    start = time.time()
    primes_new = create_constants(primes, constantDict,  copy=True)
    attrs_dict = compute_attractor_from_primes(primes_new, update_mode, initState)

    # ----------------------------------------------------
    # !!!! ---- 수정된 코드: attrs_dict 내용 상세 출력 (상태 문자열 포함) ---- !!!!
    
    # pyboolnet.state_space.state2dict import (PyBoolNet 3.x 호환성)
    from pyboolnet.state_space import state2dict as pybn_state2dict
    # stgs.state2str import (노드 순서에 따른 문자열 변환용)
    from pyboolnet.state_transition_graphs import state2str as stgs_state2str # 별칭 사용

    print("\n--- [Simulation Function] Detected Attractors for Current Perturbation ---")
    if isinstance(attrs_dict, dict) and all(isinstance(v, dict) and 'attractors' in v and 'perc' in v for v in attrs_dict.values()):
        for att_id, att_info in attrs_dict.items():
            raw_states_tuple = att_info['attractors'] # (tuple of state_strs,)
            basin_perc = att_info['perc']
            
            states_in_attractor = []
            for s_str_raw in raw_states_tuple: # '11100...' 형태의 문자열
                states_in_attractor.append(pybn_state2dict(primes, s_str_raw))
                
            if len(states_in_attractor) == 1:
                # 고정점 (Steady State)
                state_dict = states_in_attractor[0]
                state_str = stgs_state2str(state_dict) # 상태 딕셔너리를 다시 문자열로 변환
                print(f"  > Attractor ID {att_id} (Steady State, Basin {basin_perc:.2%})")
                # print(f"    State Dict: {state_dict}")
                print(f"    State Str:  {state_str}") # 추가된 부분
                
            elif len(states_in_attractor) > 1:
                # 사이클 (Cyclic Attractor)
                print(f"  > Attractor ID {att_id} (Cyclic, Length {len(states_in_attractor)}, Basin {basin_perc:.2%})")
                # print(f"    Cycle Start Dict: {states_in_attractor[0]}")
                print(f"    Cycle Start Str:  {stgs_state2str(states_in_attractor[0])}") # 추가된 부분
                # (옵션) 모든 사이클 상태를 문자열로 출력 (길면 비추)
                for j, s_dict in enumerate(states_in_attractor):
                   # print(f"       Step {j+1} Dict: {s_dict}")
                   print(f"       Step {j+1} Str:  {stgs_state2str(s_dict)}") # 추가된 부분

            else:
                print(f"  > Attractor ID {att_id} (Empty/Unknown Type, Basin {basin_perc:.2%})")
                
    else:
        print("  (Warning: Unexpected attrs_dict structure. Raw content below.)")
        print("  Raw attrs_dict content (partial):", str(attrs_dict)[:200])
        
    print("--- End of Attractor Listing ---")
    # !!!! ---- 수정된 코드 끝 ---- !!!!
    # ----------------------------------------------------

    attrs_dict = compute_phenotype(primes_new, attrs_dict, phenotype, phenotypeAnnot)
    print('Attractor simulation time :', time.time()-start)
    pheno_df = makePhenotypeDF(attrs_dict, phenotypeAnnot)
    print(makePhenotypeDF(attrs_dict, phenotypeAnnot))
    
    att_all = []
    for idx, value in enumerate(attrs_dict.values()):
        state01 = value['attractors']
        state_np = np.array([[int(x) for x in state] for state in state01])
        att1_mean = np.mean(state_np, axis=0) * value['perc']
        att_all.append(att1_mean)
    att_ave_pd = pd.DataFrame(np.sum(np.array(att_all),axis=0), index=list(primes.keys()))
    return primes_new, pheno_df, att_ave_pd, attrs_dict

