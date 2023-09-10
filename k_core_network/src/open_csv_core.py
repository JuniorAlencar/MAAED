import numpy as np
import pandas as pd
import networkx as nx

# Open graph with k_core in data
def k_core_network(k_core_number):
    df = pd.read_csv("./data/edges.csv")                                        # open file
    G = nx.from_pandas_edgelist(df,"# source", " target",create_using=nx.Graph) # Create network from data_frame
    G_ = nx.k_core(G,k=k_core_number)                                           # Define subgraph from k_core
    
    # If network isn't empty ==> return graph
    if(G_.number_of_nodes() != 0):                                                
        return G_ 
    
    # Else ==> return notification to enter with value <= k_core_max to network not empty
    else:
        g = nx.Graph()
        g.add_node(fr"empty network, please, enter with k_core <= 18")
        return g.nodes()

# Save gml_file with pairing to nodeList (open gml in gephi)
def save_network(G,k_core_number):
    node_labels = pd.read_csv("./data/nodes.csv")   # load nodeList.csv
    node_labels = node_labels.iloc[:, [0,1]] # Select just columns (index, name)
    edges = G.edges() # Create iterator about edges graph
    new_source_list = [] # New source list with name in node_label
    new_target_list = [] # New target list with name in node_label
    
    for edge in edges: # Run for all edges
        w_s = np.where(node_labels["# index"]==edge[0]) # select the line where "node_id"=element in source
        w_t = np.where(node_labels["# index"]==edge[1]) # select the line where "node_id"=element in target
        
        author_s = node_labels[" name"][w_s[0][0]]  # selects the corresponding element in the author column (source)
        author_t = node_labels[" name"][w_t[0][0]]  # selects the corresponding element in the author column (target)
        
        new_source_list.append(author_s)
        new_target_list.append(author_t)
    con__ = [(new_source_list[i],new_target_list[i]) for i in range(G.number_of_edges())] # Create new tuples in list (source,target)
    G__=nx.from_edgelist(con__) # Create graph in networkx from new tuples
    nx.write_gml(G__,f"./data/gml/k_core_{k_core_number}.gml",stringizer=None) # save network in .gml extension to read in gephi