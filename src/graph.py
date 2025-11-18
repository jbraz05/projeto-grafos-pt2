class Graph:
    def __init__(self, directed=False):
        self.adj_list = {}
        self.nodes = set()
        self.directed = directed

    def add_edge(self, u, v, weight=1.0):
        self.nodes.add(u)
        self.nodes.add(v)
        
        if u not in self.adj_list: self.adj_list[u] = {}
        if v not in self.adj_list: self.adj_list[v] = {}

        if v not in self.adj_list[u] or weight < self.adj_list[u][v]:
            self.adj_list[u][v] = weight
        
        if not self.directed:
            if u not in self.adj_list[v] or weight < self.adj_list[v][u]:
                self.adj_list[v][u] = weight

    def get_stats(self):
        # --- Lógica das estatísticas ---
        num_v = len(self.nodes)
        
        # Soma os vizinhos de todos os nós
        total_deg = sum(len(neighbors) for neighbors in self.adj_list.values())
        
        # Se não for dirigido, dividimos por 2 (pois A-B conta 2 vezes)
        num_e = total_deg if self.directed else total_deg // 2
        
        degrees = [len(self.adj_list.get(n, {})) for n in self.nodes]
        avg_deg = sum(degrees) / num_v if num_v > 0 else 0
        
        return num_v, num_e, avg_deg, degrees