from algorithms.BFS import BFS
from algorithms.DFS import DFS
from algorithms.greedy import greedy
from algorithms.A_sao import A_sao
from algorithms.Simple_Hill_Climbing import Simple_Hill_Climbing
from algorithms.Local_Beam_Search import Local_Beam_Search
from algorithms.BFS_MTPT import BFS_MTPT

ALG_MAP = {
    'BFS': BFS,
    'DFS': DFS,
    'Greedy': greedy,
    'A*': A_sao,
    'Hill Simple': Simple_Hill_Climbing,
    'Local Beam': Local_Beam_Search,
    'BFS MTPT': lambda grid, i, j: BFS_MTPT([(grid, i, j)]) 
}

def choose_algorithm(name):
    n = name.strip().lower()
    mapping = {
        "bfs": "BFS", "dfs": "DFS", "greedy": "Greedy",
        "astar": "A*", "a*": "A*", "hill simple": "Hill Simple",
        "local beam": "Local Beam",
    }
    key = mapping.get(n, None)
    if key is None:
        for k in ALG_MAP.keys():
            if k.lower() == name.lower():
                key = k
                break
    if key is None: raise ValueError(f"Unknown algorithm: {name}")
    return ALG_MAP[key]
