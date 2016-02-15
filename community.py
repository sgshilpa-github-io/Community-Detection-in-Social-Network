__author__ = 'shilpagulati'

import community as cm

import networkx as nx
import matplotlib.pyplot as plt
import operator
import itertools
import sys
from collections import defaultdict

def CalculateBetweeness(graph):

            BetweenValue=nx.edge_betweenness_centrality(graph, normalized=True,k=None,weight=None,seed=None)

            graph.remove_edges_from([k for k,v in BetweenValue.iteritems() if v == max(BetweenValue.values())])

            return graph

def partition(graph):

    graph_components = list(nx.connected_component_subgraphs(graph))

    dict={}
    len_edge=0
    for i in range(0,len(graph_components)):
        len_edge+=len(graph_components[i].edges())
        for nodes in graph_components[i].nodes():
            dict[nodes]=i

    return len_edge,dict

def main():
    G=nx.Graph()
    inputfile=sys.argv[1]
    outputimage=sys.argv[2]


    G=nx.read_edgelist(inputfile)
    G_shallow=nx.Graph(G)



    AllPartitions=[]

    len_edges =len(G.edges())

    len_edges,initiialPartition=partition(G)
    initial_mod=cm.modularity(initiialPartition,G)


    AllPartitions.append([initial_mod,initiialPartition])


    partioned_components=CalculateBetweeness(G)




    while len_edges>0:
        old_partinioned=partioned_components

        len_edges,partition_dict=partition(partioned_components)
        if len_edges==0:
            break
        mod_value=cm.modularity(partition_dict,G)

        AllPartitions.append([mod_value,partition_dict])
        partioned_components=CalculateBetweeness(partioned_components)


    li=[]
    for each in AllPartitions:
        li.append(each[0])

    indexValue= li.index(max(li))

    v = defaultdict(list)

    for key,value in sorted(AllPartitions[indexValue][1].iteritems()):
        v[value].append(key)

    n_com=len(list(v.items()))
    for key,value in sorted(v.iteritems()):
        newV=[]
        for each in value:
            newV.append(int(each))
        newV.sort()
        print newV


    pos = nx.spring_layout(G_shallow)
    for values in G_shallow.nodes():

        G_shallow.node[values]['state']=values

    map={}
    for i in range(0, n_com):
        map[i]=i/float(n_com)

    nodes_map={}
    for each in v.items():
        community=each[0]
        nodes=each[1]
        for node in nodes:
            nodes_map[node]=map[community]



    nodes_in_graph=G_shallow.nodes()
    map_of_nodes=[]
    for node in nodes_in_graph:
        map_of_nodes.append(nodes_map[node])


    node_labels = nx.get_node_attributes(G_shallow,'state')

    nx.draw(G_shallow, cmap=plt.get_cmap('rainbow'), labels=node_labels,node_color=map_of_nodes)

    plt.savefig(outputimage)
    # plt.show()



if __name__=="__main__":
    main()
