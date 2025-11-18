def dfs(graph, start_node):
    """
    Busca em Profundidade (Depth-First Search).
    Retorna a ordem de visitação.
    """
    if start_node not in graph.nodes: return []
    
    visited = set()
    traversal_order = []
    stack = [start_node]
    
    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            traversal_order.append(u)
            
            if u in graph.adj_list:
                # Adiciona vizinhos à pilha
                for v in graph.adj_list[u]:
                    if v not in visited:
                        stack.append(v)
                        
    return traversal_order