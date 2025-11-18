import csv
import os
from .graph import Graph

def load_spotify_graph(filepath):
    """
    Lê o CSV do Spotify e constrói o grafo de colaborações.
    
    Lógica de Construção:
    - Nós: Artistas.
    - Arestas: Existe se dois artistas estão na mesma música.
    - Peso: 1.000.000.000 / (streams + 1).
      (Quanto mais streams, menor o peso/distância).
    """
    print(f"... Lendo arquivo: {filepath}")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"O arquivo '{filepath}' não foi encontrado. Verifique a pasta 'data/'.")

    g = Graph(directed=False)
    
    # Tenta abrir com diferentes encodings caso dê erro
    try:
        f = open(filepath, 'r', encoding='utf-8')
    except UnicodeDecodeError:
        f = open(filepath, 'r', encoding='latin-1')

    with f:
        reader = csv.DictReader(f)
        count_rows = 0
        
        for row in reader:
            count_rows += 1
            
            # 1. Tratamento dos Artistas
            # O CSV traz algo como "Latto, Jung Kook". Separamos por vírgula.
            artists_raw = row.get('artist(s)_name', '')
            if not artists_raw: continue
            
            # Remove espaços extras
            artists = [a.strip() for a in artists_raw.split(',')]
            
            # Se tiver só 1 artista, adicionamos ele como nó isolado (opcional)
            if len(artists) == 1:
                g.nodes.add(artists[0])
                if artists[0] not in g.adj_list: g.adj_list[artists[0]] = {}
                continue

            # 2. Tratamento dos Streams (Peso)
            streams_str = row.get('streams', '0').replace(',', '')
            try:
                streams = float(streams_str)
            except ValueError:
                streams = 0.0
            weight = 1_000_000_000 / (streams + 1)
            
            for i in range(len(artists)):
                for j in range(i + 1, len(artists)):
                    g.add_edge(artists[i], artists[j], weight)

    print(f"... Processamento concluído. {count_rows} linhas lidas.")
    return g