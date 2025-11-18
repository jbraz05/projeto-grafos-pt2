from flask import Flask, jsonify, render_template, request
import os
from src.utils import load_spotify_graph
from src.algorithms import bfs, dfs, dijkstra, bellman_ford

app = Flask(__name__, template_folder='templates')

def clean_graph(g):
    """
    Remove self-loops (arestas de A para A) e nós isolados (grau 0).
    """
    # 1. Remove Self-Loops
    for u in list(g.adj_list.keys()):
        if u in g.adj_list[u]:
            del g.adj_list[u][u]

    # 2. Identifica e Remove Nós Isolados
    # (Nós que não têm vizinhos saindo E ninguém chegando neles)
    # Como seu grafo é não-dirigido na prática, basta checar a lista de adjacência.
    nodes_to_remove = []
    for node in g.nodes:
        neighbors = g.adj_list.get(node, {})
        if len(neighbors) == 0:
            nodes_to_remove.append(node)
    
    for node in nodes_to_remove:
        g.nodes.remove(node)
        if node in g.adj_list:
            del g.adj_list[node]
            
    return len(nodes_to_remove)

# --- CARREGAMENTO ---
print(">>> Carregando grafo...")
dataset_path = os.path.join('data', 'Popular_Spotify_Songs.csv')
graph = load_spotify_graph(dataset_path)

print(f">>> Nós antes da limpeza: {len(graph.nodes)}")
removed_count = clean_graph(graph)
print(f">>> Limpeza concluída! {removed_count} nós isolados removidos.")
print(f">>> Nós atuais: {len(graph.nodes)}")


def reconstruct_path(predecessors, start, end):
    """Reconstroi o caminho do fim para o começo usando o dicionário de predecessores"""
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        if curr == start: break
        curr = predecessors[curr]
        
    # Se o último adicionado não for o start, não existe caminho
    if not path or path[-1] != start:
        return []
    return path[::-1] # Inverte para ficar Start -> End


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/graph')
def get_graph_data():
    nodes = []
    edges = []
    
    # Limita envio de nós se for muito grande para o navegador não travar (opcional)
    # Aqui mandamos tudo, pois removemos os isolados
    for node in graph.nodes:
        degree = len(graph.adj_list.get(node, {}))
        nodes.append({
            'id': node, 
            'label': node, 
            'value': degree, 
            'title': f"Artista: {node} (Grau: {degree})"
        })

    added_edges = set()
    for u in graph.adj_list:
        for v, w in graph.adj_list[u].items():
            edge_key = tuple(sorted((u, v)))
            if edge_key not in added_edges:
                edges.append({'from': u, 'to': v, 'title': f"Peso: {w:.2f}"})
                added_edges.add(edge_key)

    return jsonify({'nodes': nodes, 'edges': edges})

@app.route('/api/run_algo')
def run_algorithm():
    algo_type = request.args.get('type')
    start_node = request.args.get('start')
    end_node = request.args.get('end') # Novo parâmetro
    
    if start_node not in graph.nodes:
        return jsonify({'error': 'Nó de origem inválido'}), 404

    path = []
    info = ""

    # --- BFS / DFS (Exploração) ---
    if algo_type == 'bfs':
        full_order, _ = bfs(graph, start_node)
        path = full_order # Mostra ordem de visitação
        info = f"BFS: {len(path)} nós visitados."
        
    elif algo_type == 'dfs':
        full_order = dfs(graph, start_node)
        path = full_order
        info = f"DFS: {len(path)} nós visitados."

    # --- DIJKSTRA / BELLMAN-FORD (Caminho Mínimo) ---
    elif algo_type in ['dijkstra', 'bellman_ford']:
        if not end_node or end_node not in graph.nodes:
            return jsonify({'error': 'Selecione um destino válido'}), 400
        
        t0 = 0
        dist_val = 0
        
        if algo_type == 'dijkstra':
            dists, preds = dijkstra(graph, start_node, end_node)
            dist_val = dists[end_node]
            path = reconstruct_path(preds, start_node, end_node)
            
        elif algo_type == 'bellman_ford':
            # Nota: Bellman-Ford é lento em grafos grandes, mas funciona.
            dists, preds, has_cycle = bellman_ford(graph, start_node)
            dist_val = dists[end_node]
            if has_cycle:
                info = "Ciclo negativo detectado!"
            path = reconstruct_path(preds, start_node, end_node)

        if not path:
            info = f"{algo_type.title()}: Sem caminho entre {start_node} e {end_node}."
        else:
            dist_fmt = f"{dist_val:.2f}" if dist_val != float('inf') else "Inf"
            info = f"{algo_type.title()}: Distância {dist_fmt} | {len(path)} passos."

    return jsonify({'path': path, 'info': info})

if __name__ == '__main__':
    app.run(debug=True, port=5000)