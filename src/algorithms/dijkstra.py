import heapq

def dijkstra(graph, start_node, end_node=None):
    """
    Algoritmo de Dijkstra para caminhos mínimos (pesos não-negativos).
    Retorna distâncias e predecessores.
    """
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    
    pq = [(0, start_node)]
    predecessors = {node: None for node in graph.nodes}
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        if current_dist > distances[u]: continue
        if u == end_node: break 
        
        if u in graph.adj_list:
            for v, weight in graph.adj_list[u].items():
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u
                    heapq.heappush(pq, (distances[v], v))
    
    return distances, predecessors