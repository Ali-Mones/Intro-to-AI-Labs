from collections import deque

parent_map : dict[str,str] = {}
explored : set[str] = set()
search_depth = 0

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
    global parent_map , explored , search_depth
    parent_map.clear()
    explored.clear()
    search_depth = 0
    frontier : list[str] = [init_state]
    # ask question 
    frontier_set : set[str] = set()
    frontier_set.add(init_state)
    parent_map[init_state] = init_state
    
    while  frontier :
        cur = frontier.pop()
        explored.add(cur)
        # print(cur)
        if cur == "_12345678" :
            return parent_map
        neighbours = get_neighbours(cur)
        neighbours.reverse()
        for neighbour in neighbours :
            if not (neighbour in frontier_set or neighbour in explored) :
                frontier.append(neighbour)
                frontier_set.add(neighbour)
                parent_map [neighbour] = cur
                
    return None
            
        
  
def BFS(init_state) -> dict[str,str]:
    global parent_map , explored , search_depth
    parent_map.clear()
    explored.clear()
    search_depth = 0
    frontier : deque[str] = deque()
    frontier.append(init_state)
    # ask question 
    frontier_set : set[str] = set()
    frontier_set.add(init_state)
    parent_map[init_state] = init_state
    
    while  frontier :
        cur = frontier.popleft()
        explored.add(cur)
        # print(cur)
        if cur == "_12345678" :
            return parent_map
        neighbours = get_neighbours(cur)
        for neighbour in neighbours :
            if not (neighbour in frontier_set or neighbour in explored) :
                frontier.append(neighbour)
                frontier_set.add(neighbour)
                parent_map [neighbour] = cur
                
    return None
    