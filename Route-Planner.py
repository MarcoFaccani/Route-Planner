from heapq import heappush, heappop
from math import sqrt

# ============== UTILITY METHODS ===============

def update_frontiers(frontiers, neighbours, explored):
    for neighbour in neighbours:
        if neighbour not in explored:
            frontiers[neighbour] = True

    
def add_to_explored(explored, vertex):
    explored[vertex] = True
    

def distance(exploredVertex, frontier, M):
    x1, y1 = M.intersections[exploredVertex]
    x2, y2 = M.intersections[frontier]
    distance = sqrt( (x1 - x2)**2 + (y1 - y2)**2 ) 
    return distance

def heuristic(vertex, goal, M): # small code duplication to help readability
    x1, y1 = M.intersections[vertex]
    x2, y2 = M.intersections[goal]
    distance = sqrt( (x1 - x2)**2 + (y1 - y2)**2 )
    return distance // 1.5 # optimistic heuristic
    
    
# Calculate distance from last recently explored vertex to each of its neighbours 
# and insert in the heap a new node [distance, [new_path]]
def update_pathsAndDistances(M, heap_node, frontiers, goal, heap):
   
    path = heap_node[1]
    path_distance = heap_node[0]

    for frontier in frontiers:
        heappush(heap, [path_distance + distance(path[-1], frontier, M) + heuristic(frontier, goal, M), path + [frontier] ])
    
    #Empty Frontier
    for key in list(frontiers.keys()): del frontiers[key] # maybe I can remove .keys()

        
        
# ============== MAIN METHOD ==============

def shortest_path(M,start,goal):
    
    # Valide input, make sure goal and start are nodes inside M
    if goal > len(M.intersections) -1 or start < 0:
        return None 
    
    # heap elements are made of [distance, [path]], so heap contains the current distance from start to each frontier
    explored, frontiers, heap = {}, {}, [] 
    
    cheapest_node = [0, [start]]
    
    # Search for shortest path
    while True: 
        add_to_explored(explored, cheapest_node[1][-1]) # mark node as explored
        
        if cheapest_node[1][-1] == goal:
            return cheapest_node[1] # return distance
        
        update_frontiers(frontiers, M.roads[cheapest_node[1][-1]], explored) # update frontiers of a given explored Vertex
        update_pathsAndDistances(M, cheapest_node, frontiers, goal, heap)

        cheapest_node = heappop(heap) # cheapest_node = [distance, [nodeA, nodeB, nodeC ... ] ]
