import graph
import optical
import sys

class virtual_address:
    def __init__(self):
        self.row=[]
        self.colum=[]

def short_edges():
    for edge_index in range(Gr.edges):
        for edge_index2 in range(edge_index,Gr.edges):
            if edges[edge_index2].edge_weight>edges[edge_index].edge_weight:
                temp=edges[edge_index2]
                edges[edge_index2]=edges[edge_index]
                edges[edge_index]=temp

def display_edges():
    global Gr,edges
    for edge_index2 in range(Gr.edges):
        print(f"{edges[edge_index2].source} ---> {edges[edge_index2].destination}={edges[edge_index2].edge_weight}")

def initialize_array(array):
    for index in range(Gr.nodes):
        array[index]=0

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


def hop_count(node1,node2):
    no_hops=abs(address.colum[node1]-address.colum[node2])+abs(address.row[node1]-address.row[node2])
    return no_hops 

def initialize_mapping_var(map):
    for i in range(Gr.nodes):
        map[i]=-1


def find_min_comm_pos(core_mapping_flag,node,pos,G,router_mapping_flag,inv_map):
    c=0
    min_comm=1e9
    comm=0.0
    comm_pos=[1e9]*(Gr.nodes)
    for i in range(Gr.nodes):
        comm=0
        if router_mapping_flag[i]==0:
            for j in range(Gr.nodes):
                if core_mapping_flag[j]==1:
                    ind=inv_map[j]
                    comm+=G[j][node]*hop_count(i,ind)
            comm_pos[i]=comm 
            if comm<min_comm:
                min_comm=comm 
    for j in range(Gr.nodes):
        if comm_pos[j]==min_comm:
            pos[c]=i
    return c 


def find_min_powerloss_pos(core_mapping_flag,node,pos,G,router_mapping_flag,mapping,inv_map,powerloss):
    powloss_pos=[99999999]*Gr.nodes
    min_loss=-99999999
    for node_indexl in range(Gr.nodes):
        loss_wc=-999
        if router_mapping_flag[node_indexl]==0:
            for node_index2 in range(Gr.nodes):
                if core_mapping_flag[node_index2]==1:
                    index=inv_map[node_index2]
                    loss=powerloss[index][node_indexl]
                    if loss>loss_wc:
                        loss_wc=loss
            powloss_pos[node_indexl]=loss_wc
            if loss_wc>min_loss:
                min_loss=loss_wc
    count=0
    for node_indexl in range(G.nodes):
        if powloss_pos[node_indexl]==min_loss:
            pos[count]=node_indexl
            count+=1
    return count

def find_min_SNR_pos(core_mapping_flag,node,pos,G,router_mapping_flag,mapping,inv_map,mapped_edges,powerloss,validcomm,crosstalk):
    count=0
    min_snr=-9999999999
    snr=0.0
    snr_wc=-999
    destn_flag=0
    snr,Ploss,Crosstalk=0,0,0
    srcTask,dstTask=0,0
    snr_pos=[99999999]*(Gr.nodes)
    
    temp_mapping=[]
    for i in range(Gr.rows*Gr.colums):
        temp_mapping.append(mapping[i])
    
    temp_mapped_edges=[]
    for i in range(Gr.edges):
        temp_mapped_edges.append(mapped_edges[i])
    
    for e in range(len(mapped_edges)):
        if edges[e].destination==node and inv_map[edges[e].source]!=-1:
            temp_mapped_edges[e]=1
            destn_flag=1
            break
    
    for node_indexl in range(Gr.nodes):
        snr_wc=0
        if router_mapping_flag[node_indexl]==0:
            if destn_flag==0:
                pos[0]=node_indexl
                break
            node_index2=0
            while node_index2<Gr.nodes and destn_flag:
                if core_mapping_flag[node_index2]==1:
                    #index=inv_map[node_index2]
                    temp_mapping[node_indexl]=node

                    if destn_flag==1:
                        res=optical.evaluateSNR(temp_mapping,temp_mapped_edges,powerloss,validcomm,crosstalk,snr,srcTask,dstTask,Ploss,Crosstalk,Gr,edges)
                        snr,srcTask,dstTask,Ploss,Crosstalk=res[0],res[1],res[2],res[3],res[4]

                    if snr>snr_wc and destn_flag:
                        snr_wc=snr
                node_index2+=1

            snr_pos[node_indexl]=snr_wc
            if snr_wc>min_snr and destn_flag:
                min_snr=snr_wc
    #print("min_snr",min_snr)
    count=0
    node_indexl=0
    while node_indexl<Gr.nodes and destn_flag:
        if snr_pos[node_indexl]==min_snr and destn_flag:
            pos[count]=node_indexl
            count+=1
        node_indexl+=1

    if destn_flag==0:
        return 1
    else:
        return count


def copy_arrays(source,destination):
    for i in range(Gr.nodes):
        destination[i]=source[i]

def cost(map,G):
    cost=0
    for i in range(Gr.nodes):
        for j in range(i+1,Gr.nodes):
            cost+=hop_count(i,j)*G[map[i]][map[j]]

def predict_best_pos_comm(mapping,pos,G,pos_count,node,mapping_count,core_mapping_flag,router_mapping_flag,best_map,bestcost,inv_map):
    count=0
    temp_map_count=mapping_count

    edge_index=0
    find_node=0
    temp_node=0
    index=0
    min_cost=999999
    comm_cost=0.0
    best_pos=0

    temp_pos=[0] * Gr.nodes
    temp_map=[0] * Gr.nodes
    temp_core_map_flag=[0] * Gr.nodes
    temp_router_map_flag=[0] * Gr.nodes
    temp_inv_map=[0] * Gr.nodes

    initialize_mapping_var(temp_map)
    initialize_mapping_var(temp_inv_map)
    initialize_array(temp_core_map_flag)
    initialize_array(temp_pos)
    initialize_array(temp_router_map_flag)

    while count<pos_count:
        mapping_count=temp_map_count
        temp_map=mapping[:]
        temp_core_map_flag=core_mapping_flag[:]
        temp_router_map_flag=router_mapping_flag[:]
        temp_inv_map=inv_map[:]
        
        temp_map[pos[count]]=node
        mapping_count+=1
        temp_router_map_flag[pos[count]]=1
        temp_core_map_flag[node]=1
        temp_inv_map[node]=pos[count]

        while mapping_count<Gr.nodes:
            find_node=0
            edge_index=0

            while find_node!=1:
                if get_maximum_outgoing_edge_mapped_node(temp_core_map_flag,edges[edge_index])==1:
                    temp_node=edges[edge_index].destination
                    find_node=1

                if get_maximum_outgoing_edge_mapped_node(temp_core_map_flag,edges[edge_index])==2:
                    temp_node=edges[edge_index].source
                    find_node=1

                edge_index+=1

                if edge_index==Gr.edges:
                    if find_node==0:
                        for index in range(Gr.nodes):
                            if temp_core_map_flag[index]==0:
                                temp_node=index
                                find_node=1
                                break

            initialize_array(temp_pos)
            find_min_comm_pos(temp_core_map_flag,temp_node,temp_pos,G,temp_router_map_flag,temp_map,temp_inv_map)
            temp_map[temp_pos[0]]=temp_node
            temp_core_map_flag[temp_node]=1
            temp_router_map_flag[temp_pos[0]]=1
            temp_inv_map[temp_node]=temp_pos[0]
            mapping_count+=1

        comm_cost=cost(temp_map,G)

        if comm_cost<min_cost:
            min_cost=comm_cost
            best_pos=count

        if comm_cost<bestcost:
            bestcost=comm_cost
            best_map[:]=temp_map[:]

        count+=1

    return best_pos

def predict_best_pos_PwrLoss(mapping,pos,G,pos_count,node,mapping_count,core_mapping_flag,router_mapping_flag,best_map,bestcost,inv_map,powerloss):
    count=0
    temp_map_count=mapping_count
    edge_index=0
    find_node=0
    temp_node=0
    index=0
    min_loss=-999999
    loss=0.0
    best_pos=0
    temp_pos=[0] * Gr.nodes
    temp_map=[0] * Gr.nodes
    temp_core_map_flag=[0] * Gr.nodes
    temp_router_map_flag=[0] * Gr.nodes
    temp_inv_map=[0] * Gr.nodes

    initialize_mapping_var(temp_map)
    initialize_mapping_var(temp_inv_map)
    initialize_array(temp_core_map_flag)
    initialize_array(temp_pos)
    initialize_array(temp_router_map_flag)

    while count<pos_count:
        mapping_count=temp_map_count
        temp_map=mapping[:]
        temp_core_map_flag=core_mapping_flag[:]
        temp_router_map_flag=router_mapping_flag[:]
        temp_inv_map=inv_map[:]

        temp_map[pos[count]]=node
        mapping_count+=1
        temp_router_map_flag[pos[count]]=1
        temp_core_map_flag[node]=1
        temp_inv_map[node]=pos[count]

        while mapping_count<Gr.nodes:
            find_node=0
            edge_index=0

            while find_node!=1:
                if get_maximum_outgoing_edge_mapped_node(temp_core_map_flag,edges[edge_index])==1:
                    temp_node=edges[edge_index].destination
                    find_node=1

                if get_maximum_outgoing_edge_mapped_node(temp_core_map_flag,edges[edge_index])==2:
                    temp_node=edges[edge_index].source
                    find_node=1

                edge_index+=1

                if edge_index==Gr.edges:
                    if find_node==0:
                        for index in range(Gr.nodes):
                            if temp_core_map_flag[index]==0:
                                temp_node=index
                                find_node=1
                                break

            initialize_array(temp_pos)
            find_min_powerloss_pos(temp_core_map_flag,temp_node,temp_pos,G,temp_router_map_flag,temp_map,temp_inv_map,powerloss)

            temp_map[temp_pos[0]]=temp_node
            temp_core_map_flag[temp_node]=1
            temp_router_map_flag[temp_pos[0]]=1
            temp_inv_map[temp_node]=temp_pos[0]
            mapping_count+=1

        loss =optical.evaluatePowerLoss(temp_map,powerloss,Gr,edges)

        if loss>min_loss:
            min_loss=loss
            best_pos=count

        if loss>bestcost:
            bestcost=loss
            best_map[:]=temp_map[:]

        count+=1

    return best_pos

def predict_best_pos_SNR(mapping,pos,G,pos_count,node,mapping_count,core_mapping_flag,router_mapping_flag,best_map,bestcost,inv_map,powerloss,validcomm,crosstalk):
    count=0
    temp_map_count=mapping_count
    edge_index=0
    find_node=0
    temp_node=0
    index=0
    temp_pos=[0]*(Gr.nodes)
    temp_map=[0]*(Gr.nodes)
    temp_core_map_flag=[0]*(Gr.nodes)
    temp_router_map_flag=[0]*(Gr.nodes)
    temp_inv_map=[0]*(Gr.nodes)
    mapped_edges=[-1]*(Gr.edges)

    for i in range(Gr.rows*Gr.colums):
        temp_map[i]=-1
        temp_inv_map[i]=-1
        temp_core_map_flag[i]=-1
        temp_router_map_flag[i]=-1

    initialize_mapping_var(temp_map)
    initialize_mapping_var(temp_inv_map)
    initialize_array(temp_core_map_flag)
    initialize_array(temp_pos)
    initialize_array(temp_router_map_flag)

    min_loss=999999
    loss=0
    min_snr=-99999
    best_pos=0

    while count<pos_count:
        mapping_count=temp_map_count
        copy_arrays(mapping,temp_map)
        copy_arrays(core_mapping_flag,temp_core_map_flag)
        copy_arrays(router_mapping_flag,temp_router_map_flag)
        copy_arrays(inv_map,temp_inv_map)

        temp_map[pos[count]]=node
        mapping_count+=1
        temp_router_map_flag[pos[count]]=1
        temp_core_map_flag[node]=1
        temp_inv_map[node]=pos[count]

        while mapping_count<Gr.nodes:
            find_node=0
            edge_index=0
            while find_node!=1:
                if get_maximum_outgoing_edge_mapped_node(temp_core_map_flag,edges[edge_index])==1:
                    temp_node=edges[edge_index].destination
                    find_node=1
                if get_maximum_outgoing_edge_mapped_node(temp_core_map_flag,edges[edge_index])==2:
                    temp_node=edges[edge_index].source
                    find_node=1
                elif get_maximum_outgoing_edge_mapped_node(temp_core_map_flag,edges[edge_index])==0:
                    mapped_edges[edge_index]=1
                edge_index+=1
                if edge_index==Gr.edges:
                    if find_node==0:
                        for index in range(Gr.nodes):
                            if temp_core_map_flag[index]==0:
                                temp_node=index
                                find_node=1
                                break

            initialize_array(temp_pos)
            find_min_SNR_pos(temp_core_map_flag,temp_node,temp_pos,G,temp_router_map_flag,temp_map,temp_inv_map,mapped_edges,powerloss,validcomm,crosstalk)
            #print("temp",temp_pos[0])
            temp_map[temp_pos[0]]=temp_node
            temp_core_map_flag[temp_node]=1
            temp_router_map_flag[temp_pos[0]]=1
            temp_inv_map[temp_node]=temp_pos[0]
            mapping_count+=1

        snr,Ploss,Crosstalk=0,0,0
        srcTask,dstTask=0,0
        res=optical.evaluateSNR(temp_map,mapped_edges,powerloss,validcomm,crosstalk,snr,srcTask,dstTask,Ploss,Crosstalk,Gr,edges)
        snr,srcTask,dstTask,Ploss,Crosstalk=res[0],res[1],res[2],res[3],res[4]
        if snr>min_snr:
            min_snr=snr
            best_pos=count
            copy_arrays(temp_map,best_map)
            bestcost[0]=snr
        count+=1
    return best_pos

def display_mapping(mapping):
    for row_index in range(Gr.rows):
        for colum_index in range(Gr.colums):
            print(mapping[row_index * Gr.colums+colum_index],end="\t")
        print()

def display_min_pos(pos,pos_count):
    print("positions")
    for index in range(pos_count):
        print(pos[index],end="\t")
    print()

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
        initialize_array(pos)
        if choice==0:#Communication-aware
            pos_count=find_min_comm_pos(core_mapping_flag,temp_node1,pos,G,router_mapping_flag,mapping,inv_map)
        
        elif choice==1:#Powerloss
            pos_count=find_min_powerloss_pos(core_mapping_flag,temp_node1,pos,G,router_mapping_flag,mapping,inv_map,powerloss)
        
        elif choice==2:
            pos_count=find_min_SNR_pos(core_mapping_flag,temp_node1,pos,G,router_mapping_flag,mapping,inv_map,mapped_edges,powerloss,validcomm,crosstalk)
            #print("count",pos_count)
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

def display_data(G):
    for index in range(Gr.nodes):
        for index2 in range(Gr.nodes):
            print(G[index][index2],end="\t")


def print_address(map,argument):
    inv_map=[0] * len(map)
    index=0
    fp=open("Addresses"+argument+"_Mesh_VC_Predict_PSO.txt","w")
    rout=[0]*32
    for node_index in range(len(map)):
        inv_map[map[node_index]]=node_index
    fp.write("32\n")
    for node_index in range(len(map)):
        if address.row[inv_map[node_index]]==0 and address.colum[inv_map[node_index]]==0:
            fp.write(f"c{node_index+1} 00000000 0\n")
            rout[0]=1
        elif address.row[inv_map[node_index]]==0 and address.colum[inv_map[node_index]]==1:
            fp.write(f"c{node_index+1} 10000000 1\n")
            rout[1]=1
        elif address.row[inv_map[node_index]]==1 and address.colum[inv_map[node_index]]==0:
            fp.write(f"c{node_index+1} 00001000 2\n")
            rout[2]=1
        elif address.row[inv_map[node_index]]==1 and address.colum[inv_map[node_index]]==1:
            fp.write(f"c{node_index+1} 10001000 3\n")
            rout[3]=1
        elif address.row[inv_map[node_index]]==0 and address.colum[inv_map[node_index]]==2:
            fp.write(f"c{node_index+1} 01000000 4\n")
            rout[4]=1
        elif address.row[inv_map[node_index]]==0 and address.colum[inv_map[node_index]]==3:
            fp.write(f"c{node_index+1} 11000000 5\n")
            rout[5]=1
        elif address.row[inv_map[node_index]]==1 and address.colum[inv_map[node_index]]==2:
            fp.write(f"c{node_index+1} 01001000 6\n")
            rout[6]=1
        elif address.row[inv_map[node_index]]==1 and address.colum[inv_map[node_index]]==3:
            fp.write(f"c{node_index+1} 11001000 7\n")
            rout[7]=1
        elif address.row[inv_map[node_index]]==2 and address.colum[inv_map[node_index]]==0:
            fp.write(f"c{node_index+1} 00000100 8\n")
            rout[8]=1
        elif address.row[inv_map[node_index]]==2 and address.colum[inv_map[node_index]]==1:
            fp.write(f"c{node_index+1} 10000100 9\n")
            rout[9]=1
        elif address.row[inv_map[node_index]]==3 and address.colum[inv_map[node_index]]==0:
            fp.write(f"c{node_index+1} 00001100 10\n")
            rout[10]=1
        elif address.row[inv_map[node_index]]==3 and address.colum[inv_map[node_index]]==1:
            fp.write(f"c{node_index+1} 10001100 11\n")
            rout[11]=1
        elif address.row[inv_map[node_index]]==2 and address.colum[inv_map[node_index]]==2:
            fp.write(f"c{node_index+1} 01000100 12\n")
            rout[12]=1
        elif address.row[inv_map[node_index]]==2 and address.colum[inv_map[node_index]]==3:
            fp.write(f"c{node_index+1} 11000100 13\n")
            rout[13]=1
        elif address.row[inv_map[node_index]]==3 and address.colum[inv_map[node_index]]==2:
            fp.write(f"c{node_index+1} 01001100 14\n")
            rout[14]=1
        elif address.row[inv_map[node_index]]==3 and address.colum[inv_map[node_index]]==3:
            fp.write(f"c{node_index+1} 11001100 15\n")
            rout[15]=1
        elif address.row[inv_map[node_index]]==0 and address.colum[inv_map[node_index]]==4:
            fp.write(f"c{node_index+1} 00100000 16\n")
            rout[16]=1
        elif address.row[inv_map[node_index]]==0 and address.colum[inv_map[node_index]]==5:
            fp.write(f"c{node_index+1} 10100000 17\n")
            rout[17]=1
        elif address.row[inv_map[node_index]]==1 and address.colum[inv_map[node_index]]==4:
            fp.write(f"c{node_index+1} 00101000 18\n")
            rout[18]=1
        elif address.row[inv_map[node_index]]==1 and address.colum[inv_map[node_index]]==5:
            fp.write(f"c{node_index+1} 10101000 19\n")
            rout[19]=1
        elif address.row[inv_map[node_index]]==0 and address.colum[inv_map[node_index]]==6:
            fp.write(f"c{node_index+1} 01100000 20\n")
            rout[20]=1
        elif address.row[inv_map[node_index]]==0 and address.colum[inv_map[node_index]]==7:
            fp.write(f"c{node_index+1} 11100000 21\n")
            rout[21]=1
        elif address.row[inv_map[node_index]]==1 and address.colum[inv_map[node_index]]==6:
            fp.write(f"c{node_index+1} 01101000 22\n")
            rout[23]=1
        elif address.row[inv_map[node_index]]==1 and address.colum[inv_map[node_index]]==7:
            fp.write(f"c{node_index+1} 11101000 23\n")
            rout[23]=1
        elif address.row[inv_map[node_index]]==2 and address.colum[inv_map[node_index]]==4:
            fp.write(f"c{node_index+1} 00100100 24\n")
            rout[24]=1
        elif address.row[inv_map[node_index]]==2 and address.colum[inv_map[node_index]]==5:
            fp.write(f"c{node_index+1} 10100100 25\n")
            rout[25]=1
        elif address.row[inv_map[node_index]]==3 and address.colum[inv_map[node_index]]==4:
            fp.write(f"c{node_index+1} 00101100 26\n")
            rout[26]=1
        elif address.row[inv_map[node_index]]==3 and address.colum[inv_map[node_index]]==5:
            fp.write(f"c{node_index+1} 10101100 27\n")
            rout[27]=1
        elif address.row[inv_map[node_index]]==2 and address.colum[inv_map[node_index]]==6:
            fp.write(f"c{node_index+1} 01100100 28\n")
            rout[28]=1
        elif address.row[inv_map[node_index]]==2 and address.colum[inv_map[node_index]]==7:
            fp.write(f"c{node_index+1} 11100100 29\n")
            rout[29]=1
        elif address.row[inv_map[node_index]]==3 and address.colum[inv_map[node_index]]==6:
            fp.write(f"c{node_index+1} 01101100 30\n")
            rout[30]=1
        elif address.row[inv_map[node_index]]==3 and address.colum[inv_map[node_index]]==7:
            fp.write(f"c{node_index+1} 11101100 31\n")
            rout[31]=1

    while node_index<32:
        while index<32:
            if rout[index]==0:
                fp.write(f"c{node_index+1} xx {index}\n")
                rout[index]=1
                break
            index+=1
        node_index+=1

    fp.close()


def initialize_virtual_add():
    address.row=[0]*(Gr.nodes)
    address.colum=[0]*(Gr.nodes)
    for i in range(Gr.rows):
        for j in range(Gr.colums):
            address.row[i*Gr.colums+j]=i
            address.colum[i*Gr.colums+j]=j




G=graph.initialize_graph(sys.argv[4],sys.argv[4])
Gr=graph.Gr
edges=graph.edges
#print("in main",Gr.nodes,Gr.colums,Gr.rows)
"""for x in edges:
    print(x.source,x.destination)"""
address=virtual_address()
initialize_virtual_add()
print("step 2 done")#ok

def main():
    best_map =[0]*Gr.nodes
    best_map_powerloss =[0]*Gr.nodes
    best_map_crosstalk =[0]*Gr.nodes
    mapped_edges =[0]*Gr.edges
    mapping =[0]*Gr.nodes
    bcSNR=-999

    #powerloss
    powerloss=[[0]*(Gr.rows * Gr.colums) for _ in range(Gr.rows*Gr.colums)]
    optical.read_powerloss(powerloss,int(sys.argv[4]),Gr)

    #validcomm
    validcomm=[[[[0 for i in range(Gr.rows*Gr.colums)] for j in range(Gr.rows*Gr.colums) ] for k in range(Gr.rows*Gr.colums)] for l in range(Gr.rows*Gr.colums)]
    optical.read_validcomm(validcomm,int(sys.argv[4]),Gr)

    #crosstalk
    crosstalk=[[[[0 for i in range(Gr.rows*Gr.colums)] for j in range(Gr.rows*Gr.colums) ] for k in range(Gr.rows*Gr.colums)] for l in range(Gr.rows*Gr.colums)]
    optical.read_crosstalk(crosstalk,int(sys.argv[4]),Gr)


    """print(powerloss)
    print()
    print(validcomm)
    print()
    print(crosstalk)"""
    #print(powerloss,validcomm,crosstalk)
    #verified until here
    SNR,srcTask,dstTask,Ploss,Crosstalk=0,0,0,0,0
    for index1 in range(Gr.rows):
        for index2 in range(Gr.colums):
            mapping=map_graph(int(sys.argv[5]),G,index1*Gr.colums+index2,powerloss,validcomm,crosstalk)
            display_mapping(mapping)
            x=int(sys.argv[5])

            if x==0:
                temp_cost=cost(mapping,G)
                print("Mapping Cost=",temp_cost)
                if temp_cost<best_cost:
                    best_cost=temp_cost
                    best_cost_powerloss=wcP_loss
                    copy_arrays(mapping,best_map)
            
            elif x==1:
                loss=optical.evaluatePowerLoss(mapping,powerloss,Gr,edges)
                if(wcP_loss>loss):
                    wcP_loss=loss
                    comcost_best_powerloss=temp_cost
                    copy_arrays(mapping,best_map)
                print("Mapping Cost (powerloss)=",wcP_loss)
            
            elif x==2:
                mapped_edges=[1]*(Gr.edges)
                res=optical.evaluateSNR(mapping,mapped_edges,powerloss,validcomm,crosstalk,SNR,srcTask,dstTask,Ploss,Crosstalk,Gr,edges)
                SNR,srcTask,dstTask,Ploss,Crosstalk=res[0],res[1],res[2],res[3],res[4]
                #srcTask,dstTask,Crosstalk=optical.srcTask,optical.dstTask,optical.Crosstalk
                if(bcSNR<SNR):
                    bcSNR=SNR
                    wcP_loss=Ploss
                    copy_arrays(mapping,best_map)
                print("Mapping Cost(SNR)=",SNR)
    print("\n\n************** Final mapping ****************")
    display_mapping(best_map)


    filename=f"result_Graph{sys.argv[4]}"

    output_mode=int(sys.argv[5])
    if output_mode==0:
        filename+="_Comm.txt"
    elif output_mode==1:
        filename+="_PWRLoss.txt"
    elif output_mode==2:
        filename+="_SNR.txt"

    with open(filename,"w") as outfile:
        if output_mode==0:  # Communication-aware
            temp_cost=cost(best_map,G)
            print(f"Mapping Cost (Comm)={temp_cost}")
            outfile.write(f"Mapping Cost (Comm)={temp_cost}\n")
            loss=optical.evaluatePowerLoss(best_map,powerloss,Gr,edges)
            print(f"Powerloss={loss}")
            outfile.write(f"Powerloss={loss}\n")
            mapped_edges=[1] * Gr.edges
            optical.evaluateSNR(mapping,mapped_edges,powerloss,validcomm,crosstalk,Gr,edges)
            SNR=optical.SNR
            Ploss=optical.Ploss
            srcTask,dstTask,Crosstalk=optical.srcTask,optical.dstTask,optical.Crosstalk
            print(f"SNR={SNR}")
            outfile.write(f"SNR={SNR}\n")
        
        elif output_mode==1:  # Powerloss-aware
            loss=optical.evaluatePowerLoss(best_map,powerloss,Gr,edges)
            print(f"Mapping Cost (Powerloss)={loss}")
            outfile.write(f"Mapping Cost (Powerloss)={loss}\n")
            mapped_edges=[1] * Gr.edges 
            optical.evaluateSNR(mapping,mapped_edges,powerloss,validcomm,crosstalk,Gr,edges)
            SNR=optical.SNR
            Ploss=optical.Ploss
            srcTask,dstTask,Crosstalk=optical.srcTask,optical.dstTask,optical.Crosstalk
            print(f"SNR={SNR}")
            outfile.write(f"SNR={SNR}\n")
        
        elif output_mode==2:  # SNR-aware
            mapped_edges=[1] * Gr.edges
            res=optical.evaluateSNR(mapping,mapped_edges,powerloss,validcomm,crosstalk,SNR,srcTask,dstTask,Ploss,Crosstalk,Gr,edges)
            SNR,srcTask,dstTask,Ploss,Crosstalk=res[0],res[1],res[2],res[3],res[4]
            print(f"Mapping Cost (SNR)={SNR}")
            outfile.write(f"Mapping Cost (SNR)={SNR}\n")
            print(f"Powerloss={Ploss}")
            outfile.write(f"Powerloss={Ploss}\n")

    outfile.close()
                

                        

if __name__ == "__main__":
    main()
                    









    