from src.create_network import *
import random
import numpy as np
import math

def are_multiples(number, factor):
    return number % factor == 0
    #return [num % factor == 0 for num in numbers]

def random_attack(G,num_divisions):
    N_nodes = len([v for v in G.nodes()])
    
    num_nodes_largest = []
    num_nodes_remove = []
    
    for i in range(N_nodes):
        nodes = [v for v in G.nodes()]
        node_random = random.choice(nodes)
        G.remove_node(node_random)
        conditional = are_multiples(len(nodes), num_divisions)
        if(conditional==True):
            components = list(nx.connected_components(G))
            largest_component = max(components, key=len)
            largest_subgraph = G.subgraph(largest_component)
            nodes = [v for v in largest_subgraph.nodes()]
            num_nodes_largest.append(len(nodes))
            num_nodes_remove.append(i)
    
    num_nodes_largest = [i/N_nodes for i in num_nodes_largest]
    num_nodes_remove = [i/N_nodes for i in num_nodes_remove]

    return num_nodes_remove, num_nodes_largest

def random_attack_samples(num_samples, num_divisions):
    my_dict_remove = {}
    my_dict_N_nodes = {}

    for i in range(num_samples):
        G = create_network()
        f, sf = random_attack(G, num_divisions)
        my_dict_N_nodes[f"sample_{i}"] = sf
        my_dict_remove[f"sample_{i}"] = f
    df_nodes = pd.DataFrame(data=my_dict_N_nodes)
    df_remove = pd.DataFrame(data=my_dict_remove)
    
    return df_nodes, df_remove

def random_attack_mean(df_nodes, df_remove):
    nodes_mean = df_nodes.mean(axis=1)
    nodes_erro_mean = df_nodes.sem(axis=1)

    remove_mean = df_remove.mean(axis=1)
    
    # The number of remove nodes don't changer, so don't erro in N_remove
    data_nodes = {"N_nodes":nodes_mean.values,"N_error":nodes_erro_mean.values}
    data_remove = {"N_remove":remove_mean.values}
    
    df_mean_node = pd.DataFrame(data=data_nodes)
    df_mean_remove = pd.DataFrame(data=data_remove)
    
    df_mean_node.to_csv("../data/attack_network/N_node_random_attack.csv",index=False)
    df_mean_remove.to_csv("../data/attack_network/N_remove_random_attack.csv",index=False)

    return df_mean_node, df_mean_remove