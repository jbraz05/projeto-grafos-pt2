from collections import deque

def bfs(graph, start_node):
    """
    Busca em Largura (Breadth-First Search).
    Retorna a ordem de visitação e um dicionário com as camadas (distância em arestas).
    """
    if start_node not in graph.nodes: return [], {}
    
    visited = {start_node}
    queue = deque([(start_node, 0)])
    traversal_order = []
    layers = {}
    
    while queue:
        u, layer = queue.popleft()
        traversal_order.append(u)
        layers[u] = layer
        
        if u in graph.adj_list:
            for v in graph.adj_list[u]:
                if v not in visited:
                    visited.add(v)
                    queue.append((v, layer + 1))
                    
    return traversal_order, layers