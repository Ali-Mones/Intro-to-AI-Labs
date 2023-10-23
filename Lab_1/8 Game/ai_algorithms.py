from collections import deque
from queue import PriorityQueue
from math import sqrt

parent_map : dict[str,str] = {}
explored : set[str] = set()
depth: int = 0
nodes_expanded = 0


def get_neighbours (state) ->list[str] :
    pos = 0
    for i in range(9):
        if state[i] == "_" :
            pos = i
            break 
    neighbours : list[str] = []
    temp = list(state)
    #----------up------
    if pos//3==0 or pos//3==1:
        temp[pos] = temp[pos+3]
        temp[pos+3] = "_"
        neighbours.append("".join(temp))
        temp = list(state)
    #-------down-----
    if pos//3==1 or pos//3==2:
        temp[pos] = temp[pos-3]
        temp[pos-3] = "_"
        neighbours.append("".join(temp))
        temp = list(state)
    # --------left---------
    if pos%3==0 or pos%3==1:
        temp[pos] = temp[pos+1]
        temp[pos+1] = "_"
        neighbours.append("".join(temp))
        temp = list(state)
    #----------right-------        
    if pos%3==1 or pos%3==2:
        temp[pos] = temp[pos-1]
        temp[pos-1] = "_"
        neighbours.append("".join(temp))
    return neighbours


# ----------------DFS----------------------
def DFS(init_state) -> dict[str,str]:
    global parent_map , explored , search_depth, depth, nodes_expanded
    depth = 0
    nodes_expanded=0
    parent_map.clear()
    explored.clear()
    frontier : list[(str, int)] = [(init_state, 0)]
    # ask question 
    frontier_set : set[str] = set()
    frontier_set.add(init_state)
    parent_map[init_state] = init_state
    
    while  frontier :
        cur, level = frontier.pop()
        nodes_expanded+=1
        depth=max(depth, level)
        explored.add(cur)
        # print(cur)
        if cur == "_12345678" :
            return parent_map
        neighbours = get_neighbours(cur)
        neighbours.reverse()
        for neighbour in neighbours :
            if not (neighbour in frontier_set or neighbour in explored) :
                frontier.append((neighbour, level+1))
                frontier_set.add(neighbour)
                parent_map [neighbour] = cur
                
    return None
            
        
# ----------------BFS---------------------- 
def BFS(init_state) -> dict[str,str]:
    global parent_map , explored , search_depth, depth, nodes_expanded
    depth = 0
    nodes_expanded=0
    parent_map.clear()
    explored.clear()
    frontier : deque[(str, int)] = deque()
    frontier.append((init_state, 0))
    # ask question 
    frontier_set : set[str] = set()
    frontier_set.add(init_state)
    parent_map[init_state] = init_state  
    while  frontier :
        cur, level = frontier.popleft()
        depth = max(depth, level)
        explored.add(cur)
        nodes_expanded+=1
        # print(cur)
        if cur == "_12345678" :
            return parent_map
        neighbours = get_neighbours(cur)
        for neighbour in neighbours :
            if not (neighbour in frontier_set or neighbour in explored) :
                frontier.append((neighbour, level+1))
                frontier_set.add(neighbour)
                parent_map [neighbour] = cur
                
    return None


# ---------------Utilities--------------------------
def getpos(pos):
    row = pos//3
    col = pos%3
    return (row,col)


# ----------------A* Manhattan----------------------     
def M_Heuristic(state:str):
    
    heuristic:int = 0
    for i in range(len(state)):
        if(state[i] != '_'):
            curr_pos = getpos(i)
            req_pos =  getpos(ord(state[i])-ord('0'))
            dist = abs(curr_pos[0]-req_pos[0]) + abs(curr_pos[1]-req_pos[1])
            heuristic+=dist

    return heuristic
             
def AStarManhattan(init_state:str) -> dict[str,str]:
    global parent_map , explored , search_depth, depth, nodes_expanded
    parent_map.clear()
    explored.clear()
    search_depth = 0
    Pmap:dict[str,tuple(str,int)] = {}
    frontier : PriorityQueue[tuple(int,str)] = PriorityQueue()
    init_heur = M_Heuristic(init_state)
    frontier.put((init_heur,init_state))
    # ask question 
    frontier_set : set[str] = set()
    frontier_set.add(init_state)
    Pmap[init_state] = (init_state,0)
    parent_map[init_state] = init_state
    
    while frontier:
        
        f,state = frontier.get()
        G = f - M_Heuristic(state)
        if(state in explored):
            continue
        
        explored.add(state)
        if state == "_12345678" :
            nodes_expanded = len(explored)
            return parent_map
        
        neighbours = get_neighbours(state)
        for neighbour in neighbours : 
            if not (neighbour in frontier_set or neighbour in explored) :
                heur = M_Heuristic(neighbour)
                cost = G + 1 + heur
                frontier.put((cost,neighbour))
                frontier_set.add(neighbour)
                parent_map[neighbour] = state
                Pmap[neighbour] = (state,G + 1)
            elif neighbour in frontier_set:
                if(G + 1 < Pmap[neighbour][1]):
                    Pmap[neighbour] = (state,G+1)   
                    parent_map[neighbour] = state 
                         
    nodes_expanded = len(explored)
    return None 

# ----------------A* Euclidean---------------------- 
def E_Heuristic(state:str):
    
    heuristic:float = 0
    for i in range(len(state)):
        if(state[i] != '_'):
            curr_pos = getpos(i)
            req_pos =  getpos(ord(state[i])-ord('0'))
            dist = sqrt(pow(curr_pos[0]-req_pos[0],2) + pow(curr_pos[1]-req_pos[1],2))
            heuristic+=dist
    
    return heuristic        
            
def AStarEuclidean(init_state:str) -> dict[str,str]:
    global parent_map , explored , search_depth, depth, nodes_expanded
    parent_map.clear()
    explored.clear()
    search_depth = 0
    Pmap:dict[str,tuple(str,int)] = {}
    frontier : PriorityQueue[tuple(int,str)] = PriorityQueue()
    init_heur = E_Heuristic(init_state)
    frontier.put((init_heur,init_state))
    # ask question 
    frontier_set : set[str] = set()
    frontier_set.add(init_state)
    Pmap[init_state] = (init_state,0)
    parent_map[init_state] = init_state
    
    while frontier:
        
        f,state = frontier.get()
        G = f - E_Heuristic(state)
        if(state in explored):
            continue
        
        explored.add(state)
        if state == "_12345678" :
            nodes_expanded = len(explored)
            return parent_map
        
        neighbours = get_neighbours(state)
        for neighbour in neighbours : 
            if not (neighbour in frontier_set or neighbour in explored) :
                heur = E_Heuristic(neighbour)
                cost = G + 1 + heur
                frontier.put((cost,neighbour))
                frontier_set.add(neighbour)
                parent_map[neighbour] = state
                Pmap[neighbour] = (state,G + 1)
            elif neighbour in frontier_set:
                if(G + 1 < Pmap[neighbour][1]):
                    Pmap[neighbour] = (state,G+1)   
                    parent_map[neighbour] = state 
                         
    nodes_expanded = len(explored)
    return None 
