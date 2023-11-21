import networkx as nx
import pandas as pd
import collections
import numpy as np

# create dataframe assortativity
def assortativity_create(G):
    degrees = G.degree()
    nodes = [d for d,v in degrees]
    degree = [v for d,v in degrees]
    k_ij = []
    for i in range(len(nodes)):
        denominator = degrees[nodes[i]]
        # for some reason exist 1 node exist loop with youself
        if (denominator==0):
            G.remove_node(nodes[i])
            pass
        else:
            degreekij = [degrees[j] for j in [n for n in G.neighbors(nodes[i])]]
            Ter = sum(degreekij)/denominator
            k_ij.append(Ter)
    data = {"degree":degree,"k_ij":k_ij}
    df = pd.DataFrame(data=data)
    df.to_csv("../data/assortativity.csv",index=False,mode="w")
    return df

# Calcule x and y in log-bin

def drop_zeros(a_list):
    return [i for i in a_list if i>0]

def binning_2d(x, y,num_bins):
    x_bin, y_bin = [], []
    counter_dict = collections.Counter(x)
    
    max_x = np.log10(max(list(counter_dict.keys())))
    max_y = np.log10(max(list(counter_dict.values())))
    max_base = max([max_x,max_y])
    min_x = np.log10(min(drop_zeros(list(counter_dict.keys()))))

    bins_aux = np.logspace(min_x,max_base,num=num_bins)
    bins = [(bins_aux[q],bins_aux[q+1]) for q in range(len(bins_aux)-1)]

    box_bins_k = [[] for _ in range(len(bins))]
    box_bins_knn = [[] for _ in range(len(bins))]

    for l in range(len(x)):
        for m in range(len(bins)):
            if(bins[m][0]<=x[l]<=bins[m][1]):
                box_bins_k[m].append(x[l])
                box_bins_knn[m].append(y[l])
    
    index_list = []
    for idk,element in enumerate(box_bins_k):
        if(len(element)!=0):
            index_list.append(idk)

    box_bins_k = [box_bins_k[q] for q in index_list]
    box_bins_knn = [box_bins_knn[q] for q in index_list]

    x_bin = [np.mean(box_bins_k[q]) for q in range(len(box_bins_k))]
    y_bin = [np.mean(box_bins_knn[q]) for q in range(len(box_bins_knn))]
    return x_bin,y_bin