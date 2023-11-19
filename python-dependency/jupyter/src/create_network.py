import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import csv

# Function to create network with networkX

def create_network():
    # Crie um objeto de grafo direcionado (ou não direcionado, dependendo de seus dados)
    G = nx.Graph()  # Grafo direcionado

    # Leitura do arquivo nodes.csv
    with open('../data/nodes.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # Adicione nós ao grafo
        for row in csv_reader:
            node_id = row[0]
            # Você pode adicionar mais atributos aos nós se houver mais informações no arquivo CSV
            G.add_node(node_id)

    # Leitura do arquivo edges.csv
    with open('../data/edges.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # Adicione arestas ao grafo
        for row in csv_reader:
            source_node = row[0]
            target_node = row[1]
            # Você pode adicionar mais atributos às arestas se houver mais informações no arquivo CSV
            G.add_edge(source_node, target_node)

    # Agora você tem um objeto de grafo NetworkX representando sua rede.
    # Você pode realizar várias operações de análise e visualização com esse objeto.
    df_edge = pd.read_csv('../data/edges.csv', dtype={'package': str,"requirement":str})
    # Create network with dataframe
    G = nx.from_pandas_edgelist(df_edge,"package", "requirement",create_using=nx.Graph)
    G.remove_edges_from(nx.selfloop_edges(G))
    return G

