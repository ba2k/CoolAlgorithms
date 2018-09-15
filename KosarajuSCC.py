
# coding: utf-8

# # Computing Strongly Connected Components
# 
# ### Kosaraju's algorithm's 2 DFS Pass Algorithm
# 
# strongly connected componenets, are maximum regions in a directed graph that we can get from any one point to other points and vise versa.

# #### Constructs Vertices-Representation of given graph file represented by its Edges

# In[ ]:


def load_graph(file_name):
    
    V = {}
    
    # read graph file line by line i.e. one edge(u, v) at a time, process and add it to V
    with open(file_name, 'r') as graph_file:
        
        for line in graph_file:
            
            edge = line.strip().split() # list of strings
            edge = list(map(int, edge)) # list of ints
            
            # addind vertex u info
            u = edge[0]
            v = edge[1]
            w = [v, True]
            if u in V:
                V[u][0].append(w)
            else:
                V[u] = [[w], 0, u]
            
            # addind vertex v info
            u, v = v, u
            w = [v, False]
            if u in V:
                V[u][0].append(w)
            else:
                V[u] = [[w], 0, u]
            
    return V 


# #### Depth First Search 

# In[ ]:


def DFS(V, start, kasaraju_1st_pass):

    stack = []
    V[start][1] = True 
    stack.append(V[start])
    
    global discovered_scc_vertices
    discovered_scc_vertices = []
    
    while stack:
        
        v = stack.pop()
        neighbors = v[0]    
        neighbors_cnt = len(neighbors)
        
        for i in neighbors:
            
            next_neighor = i[0]
            if kasaraju_1st_pass:  
                direction = not i[1]    
            else: 
                direction =  i[1] 
                
            neighbors_cnt -= 1

            if (V[next_neighor][1] != True) and direction:
                
                discovered_scc_vertices.append(next_neighor)
                
                V[next_neighor][1] = True
                stack.append(v)
                stack.append(V[next_neighor])
                break
                
            if kasaraju_1st_pass and (neighbors_cnt == 0):
                finish_order_stack.append(v)
                    
    return V


# In[ ]:


graph_file = 'graph.txt'
Graph = load_graph(graph_file)


# ### Kosaraju 1st DFS on Transposed Graph
# 
# This DFS pass computes finishing time of each vertex, on the "transpose graph" (the same graph with the direction of every edge reversed). This is to get each vertices sorted/ordered by thier finish time to be provided/followed to 2nd DFS pass.

# In[ ]:


finish_order_stack = []

first_pass = True
for vertex in range(len(Graph), 0, -1):
    if Graph[vertex][1] != True:
        Graph = DFS(Graph, vertex, first_pass)


# In[ ]:


# resert vertices to unexplored for 2nd DFS
for vertex in Graph:
    Graph[vertex][1] = False


# ### Kosaraju 2nd DFS from Last-Finished Vertex in 1st-Pass 
# 
# Invoking DFS from the highest order (last finishing time vertex computed in the 1st pass), decreasing one at the time, to the last vertex in original/forward graph while keeping track of the leaders vertices whice are the SCCs. Everytime we invoke DFS the vertices discovered are percisely one of the newly discovered SCCs. Each SSC present itself one per DFS call.

# In[ ]:


SCCs = []
for i in range(len(Graph)):
    vertex = finish_order_stack.pop()
    if vertex[1] != True:
        
        vertex[1] = True
        scc_leader = vertex[2]
        scc_size = len(discovered_scc_vertices) + 1
        SCCs.append((scc_size, scc_leader))
        
        DFS(Graph, scc_leader, not first_pass)


# In[ ]:


# print top 5 largest SCCs (size, leader)
print(sorted(SCCs, reverse=True)[:5])

