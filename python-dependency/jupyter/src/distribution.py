from collections import Counter
import numpy as np
import pandas as pd
import networkx as nx

def distribution_top10():
    df_edge = pd.read_csv('../data/edges.csv', dtype={'package': str,"requirement":str})
    df_node = pd.read_csv('../data/nodes.csv', dtype={'index': str,"requirement":str})
    # Create network with dataframe
    G = nx.from_pandas_edgelist(df_edge,"package", "requirement",create_using=nx.Graph)
    
    # Create dictionary with ('node',degree) in descending order
    degrees = dict(G.degree())
    degree_sequence = [v for d,v in G.degree()]
    sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)

    # Top 10 nodes and their degrees
    degree_10 = [sorted_nodes[i][0] for i in range(10)]
    node_10 = [sorted_nodes[i][1] for i in range(10)]
    node_label_10 = [df_node["package"][df_node["index"]==degree_10[i]].values[0] for i in range(10)]
    return node_label_10, node_10, degree_sequence

# Calcule the distribution of degree
def distribution(degree):
    hist, bins_edge = np.histogram(degree, bins=np.arange(0.5,10**4+1.5,1), density=True)
    
    P = hist*np.diff(bins_edge)             # distribution = density*deltaK
    K = bins_edge[:-1]+bins_edge[:1]
    index_remove = []                       # load index with distribution zero
    
    for idk,elements in enumerate(P):
        if(elements==0):
            index_remove.append(idk) 
    # Removing elements in k_mean and distribution with distribution = 0 (empty box)
    p_real = np.delete(P,index_remove)      
    k_real = np.delete(K,index_remove)
    return k_real,p_real

