class graph_info:
    def __init__(self):
        self.nodes=0
        self.rows=0
        self.colums=0
        self.edges=0

class edge_info:
    def __init__(self):
        self.source=0
        self.destination=0
        self.edge_weight=0.0

class virtual_address:
    def __init__(self):
        self.row=[]
        self.colum=[]

global Gr
Gr=graph_info()
global edges




def read_graph(G,data):
    file_name = "Graph"+str(data)+".txt"
    with open(file_name, 'r') as fp:
        rows=int(fp.readline())
        ind=0
        #print(len(G),len(G[0]))
        while(ind<Gr.nodes):
            a=fp.readline()
            #print(a)
            # tmp=a.split("\t")
            tmp = a.split('\t') if '\t' in a else a.split()
            #print(tmp)
            column=0
            marker=0
            while marker<(Gr.nodes):
                if tmp[column]=="":
                    column+=1
                    continue
                elif tmp[column]=="INF" or tmp[column]=="INF\n":
                    tmp[column]=0
                else:
                    Gr.edges+=1
                #print(tmp[column])
                G[ind][marker]=float(tmp[column])
                column+=1
                marker+=1
            ind+=1
    #print(G)
    Gr.edges = Gr.edges//2



def map_graph(choice,G,router_id,powerloss,validcomm,crosstalk):
    mapping_count=0
    edge_index=0
    best_pos=0
    minpowerloss=9999

    router_mapping_flag=[0]*(Gr.rows * Gr.colums)
    core_mapping_flag=[0]*(Gr.nodes)
    mapped_edges=[0]*(Gr.edges)
    pos=[0]*(Gr.nodes)
    mapping=[0]*(Gr.rows*Gr.colums)
    best_map=[0]*(Gr.rows*Gr.colums)
    inv_map=[0]*(Gr.rows*Gr.colums)
    bestcost=[999999]
    if choice==0:
        bc=999999
        bestcost[0]=bc
    elif choice==1 or choice==2:
        bc=-999999
        bestcost[0]=bc 
    
    initialize_array(router_mapping_flag)
    initialize_mapping_var(mapping)
    initialize_array(core_mapping_flag)

    temp_node1=edges[0].destination
    temp_node2=edges[0].source

    for i in range(Gr.rows*Gr.colums):
        inv_map[i]=-1
        mapping[i]=-1

    for i in range(Gr.edges):
        mapped_edges[i]=-1

    if get_comm_of_node(temp_node1,G)>get_comm_of_node(temp_node2,G):
        mapping[router_id]=temp_node1
        core_mapping_flag[temp_node1]=1
        inv_map[temp_node1]=router_id
    else:
        mapping[router_id]=temp_node2
        core_mapping_flag[temp_node2]=1
        inv_map[temp_node2]=router_id

    router_mapping_flag[router_id]=1
    mapping_count+=1

    #print(mapping)
    #print(core_mapping_flag)
    #print(inv_map)

    while mapping_count<Gr.nodes:
        find_node=0
        edge_index=0
        while find_node!=1:
            if get_maximum_outgoing_edge_mapped_node(core_mapping_flag,edges[edge_index])==1:
                temp_node1=edges[edge_index].destination
                find_node=1
            elif get_maximum_outgoing_edge_mapped_node(core_mapping_flag,edges[edge_index])==2:
                temp_node1=edges[edge_index].source
                find_node=1
            
            elif get_maximum_outgoing_edge_mapped_node(core_mapping_flag,edges[edge_index])==0:
                mapped_edges[edge_index]=1
            edge_index+=1

            if edge_index==Gr.edges:
                if find_node==0:
                    for index in range(Gr.nodes):
                        if core_mapping_flag[index]==0:
                            temp_node1=index
                            find_node=1
                            break
        #ok until here
        pos_count = 0
        initialize_array(pos)
        if choice==0:#Communication-aware
            pos_count=find_min_comm_pos(core_mapping_flag,temp_node1,pos,G,router_mapping_flag,mapping,inv_map)
        
        elif choice==1:#Powerloss
            pos_count=find_min_powerloss_pos(core_mapping_flag,temp_node1,pos,G,router_mapping_flag,mapping,inv_map,powerloss)
        
        elif choice==2:
            pos_count=find_min_SNR_pos(core_mapping_flag,temp_node1,pos,G,router_mapping_flag,mapping,inv_map,mapped_edges,powerloss,validcomm,crosstalk)
            print("count",pos_count)
        buff=0

        if pos_count>1:
            if choice==0:#Communication-aware
                best_pos=predict_best_pos_comm(mapping,pos,G,pos_count,temp_node1,mapping_count,core_mapping_flag,router_mapping_flag,best_map,bestcost,inv_map)
            
            elif choice==1:#Powerloss
                best_pos=predict_best_pos_PwrLoss(mapping,pos,G,pos_count,temp_node1,mapping_count,core_mapping_flag,router_mapping_flag,best_map,bestcost,inv_map,powerloss)
            
            elif choice==2:#SNR
                best_pos=predict_best_pos_SNR(mapping,pos,G,pos_count,temp_node1,mapping_count,core_mapping_flag,router_mapping_flag,best_map,bestcost,inv_map,powerloss,validcomm,crosstalk)
                #print("bestpos",best_pos)
            mapping[pos[best_pos]]=temp_node1
            core_mapping_flag[temp_node1]=1
            router_mapping_flag[pos[best_pos]]=1
            inv_map[temp_node1]=pos[best_pos]
            mapping_count+=1
        else:
            mapping[pos[0]]=temp_node1
            core_mapping_flag[temp_node1]=1
            router_mapping_flag[pos[0]]=1
            inv_map[temp_node1]=pos[0]
            mapping_count+=1
    #print(mapping)
    return mapping

def initialize_graph_info(no_nodes,no_rows,no_columns,no_edges):
    Gr.nodes=no_nodes
    Gr.rows=no_rows
    Gr.colums=no_columns
    Gr.edges=no_edges

def allocate_memory(no_nodes):
    graph=[[0 for _ in range(no_nodes)] for _ in range(no_nodes)]
    return graph

def copy_graph(graph,temp_graph,no_nodes):
    for node_index1 in range(no_nodes):
        for node_index2 in range(no_nodes):
            graph[node_index1][node_index2]=temp_graph[node_index1][node_index2]

def find_edges(graph,no_nodes):
    no_edges=0
    for node_index1 in range(no_nodes):
        for node_index2 in range(node_index1 + 1,no_nodes):
            if graph[node_index1][node_index2]!= 0:
                no_edges += 1
    return no_edges


def initialize_edges(graph,edges,n):
    edge_index=0
    for node_index1 in range(Gr.nodes):
        for node_index2 in range(node_index1,Gr.nodes):
            if graph[node_index1][node_index2]!=0:
                edges[edge_index].source=node_index1
                edges[edge_index].destination=node_index2
                edges[edge_index].edge_weight=graph[node_index1][node_index2]
                edge_index+=1
        
def initialize_array(array):
    for index in range(Gr.nodes):
        array[index]=0

def initialize_mapping_var(map):
    for i in range(Gr.nodes):
        map[i]=-1

def get_comm_of_node(node,G):
    comm=0.0
    for node_index in range(Gr.nodes):
        comm+=G[node][node_index]
    return comm

def get_maximum_outgoing_edge_mapped_node(core_mapping_flag,edge):
    if core_mapping_flag[edge.source] & core_mapping_flag[edge.destination]:
        return 0
    elif core_mapping_flag[edge.source]:
        return 1
    elif core_mapping_flag[edge.destination]:
        return 2
    else:
        return 3

def initialize_graph(arg,name):
    choice=int(arg)
    divider=2
    if choice==3:
        no_nodes=8
        no_rows=2
        no_columns=4
        graph=allocate_memory(no_nodes)

    if choice==15:
        no_nodes=16
        no_rows=4
        no_columns=4
        graph=allocate_memory(no_nodes)

    if choice in [1,5,6,7,8,9,10,14,2]:
        no_nodes=12
        no_rows=4
        no_columns=3
        graph=allocate_memory(no_nodes)

    if choice==4:
        no_nodes=32
        no_rows=4
        no_columns=8
        graph=allocate_memory(no_nodes)

    if choice==12:
        no_nodes=24
        no_rows=4
        no_columns=6
        graph=allocate_memory(no_nodes)

    if choice==13:
        no_nodes=30
        no_rows=5
        no_columns=6
        graph=allocate_memory(no_nodes)

    if choice in [17,18,19,20,21,22,23]:
        no_nodes=64
        no_rows=8
        no_columns=8
        graph =allocate_memory(no_nodes)

    if choice in [25,26,27,28,29,30]:
        no_nodes=128
        no_rows=8
        no_columns=16
        graph=allocate_memory(no_nodes)

    initialize_graph_info(no_nodes,no_rows,no_columns,0)
    read_graph(graph,choice)
    #print(graph)
    for node_index1 in range(no_nodes):
        for node_index2 in range(node_index1 + 1,no_nodes):
            graph[node_index1][node_index2]=(graph[node_index1][node_index2]+graph[node_index2][node_index1])/divider
            graph[node_index2][node_index1]=graph[node_index1][node_index2]
    
    #print(graph)
    no_edges=find_edges(graph,no_nodes)
    initialize_graph_info(no_nodes,no_rows,no_columns,no_edges)
    global edges
    edges=[edge_info() for _ in range(no_edges)]
    #print(edges,no_edges)
    initialize_edges(graph,edges,no_edges)
    """for x in edges:
        print(x.source,x.destination,x.edge_weight)"""
    return graph