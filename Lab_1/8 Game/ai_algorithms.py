from collections import deque

parent_map : dict[str,str] = {}
explored : set[str] = set()
depth: int = 0
nodes_expanded = 0


def get_neighbours (state ) ->list[str] :
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
