import sys
import random
import math
import Header
# from SNR import main as snrmain
from Header import *


TILE_WIDTH = 0.0025  # IN DIRECTION OF COLUMN
TILE_HEIGHT = 0.0025  # IN DIRECTION OF ROWS
NO_OF_RUN = 1

# Global variables
a = None  # Initialize as needed
cost_best = 99999999
save_partition = None  # Initialize as needed

class GraphInfo:
    def __init__(self):
        self.No_nodes = 0
        self.actual_No_nodes = 0
        self.rows = 0
        self.columns = 0
        self.edges = 0

Graph_inf = GraphInfo()

class Commodity:
    def __init__(self):
        self.value = 0.0
        self.source = 0
        self.destination = 0


import math

def initialize_add():
    global a
    nodes = Graph_inf.No_nodes
    n4 = math.log(nodes) / math.log(2.0)
    # print(n4)
    n = int(n4)
    row_add = [0] * nodes
    col_add = [0] * nodes
    tmp = [[0] * nodes for _ in range(n - 1)]
    
    for i in range(1, n):
        c = 0
        l = 0
        for j in range(2 ** i):
            for k in range(2 ** (n - i)):
                tmp[i - 1][l] = c
                l += 1
            c += 1
    for i in range(0, nodes, 4):
        row_add[i] = col_add[i] = row_add[i + 1] = col_add[i + 2] = 0
        col_add[i + 1] = row_add[i + 2] = col_add[i + 3] = row_add[i + 3] = 1

    count = 0 
    xyz = 1
    for i in range(4, nodes, i * 4):
        count = 0
        xyz = xyz * 2
        j = 0
        while i * count < nodes:
            j = j % 4
            for k in range(i):
                if k < i and i * count + k < nodes:
                    if j == 2 or j == 3:
                        row_add[i * count + k] += xyz
                    if j == 1 or j == 3:
                        col_add[i * count + k] += xyz
            j+=1
            count+=1



    address.colum = col_add
    address.row = row_add
    a = tmp


def read_graph(name, dist):
    fp1 = open(name, 'r')

    nodes = int(fp1.readline().strip())
    # buff = fp1.readline().strip()

    Graph_inf.actual_No_nodes = actual_no_of_nodes = nodes
    Graph_inf.edges = 0

    n2 = math.log(nodes) / math.log(2.0)
    n1 = int(n2)
    print(f"{n1} {n2} actual nodes {nodes}")

    if n2 > float(n1):
        print("\n\t\tAdding dummy nodes\n")
        n3 = pow(2.0, n1 + 1)
        nodes = int(n3)
        print(f"\nincluding dummy nodes= {nodes}\n")

    row = 0
    co = 0
    count = 0
    netlist = [0.0] * nodes

    # Allocate memory for each inner list
    for i in range(nodes):
        netlist[i] = [0.0] * nodes
    
    # print(type(netlist[0][0]))
    for row in range(actual_no_of_nodes):
        buff = fp1.readline().strip().split()

        for co, val in enumerate(buff):
            if val and "INF" not in val:
                z = float(val)
            else:
                z = 0.0
            netlist[row][co] = z


    temp_pow = math.log(nodes) / math.log(2.0)
    split1 = math.floor(temp_pow / 2.0)
    split2 = math.ceil(temp_pow / 2.0)
    Graph_inf.No_nodes = nodes
    Graph_inf.rows = int(pow(2, split1))
    Graph_inf.colums = int(pow(2, split2))

    print(f"\n rows {Graph_inf.rows}\n cols {Graph_inf.colums}\n")
    fp1.close()
    distri = int(dist)

    if n2 > float(n1) and distri == 1:
        # Fill 0s in dummy rows
        for i in range(actual_no_of_nodes, nodes):
            for j in range(nodes):
                if j >= actual_no_of_nodes:
                    netlist[i][j] = 0.0
                else:
                    netlist[i][j] = 0.0

        # Fill 0s in dummy cols
        for i in range(actual_no_of_nodes):
            for j in range(actual_no_of_nodes, nodes):
                netlist[i][j] = 0.0

        # Fill 0s in Diagonal
        for i in range(nodes):
            netlist[i][i] = 0.0

    elif n2 > float(n1):
        for i in range(actual_no_of_nodes, nodes):
            for j in range(nodes):
                if j >= actual_no_of_nodes:
                    netlist[i][j] = MAX
                else:
                    netlist[i][j] = 0.0

        for i in range(actual_no_of_nodes):
            for j in range(actual_no_of_nodes, nodes):
                netlist[i][j] = 0.0

        for i in range(nodes):
            netlist[i][i] = 0.0

    return netlist



def main():

    t = time.time()
    random.seed(t)

    if len(sys.argv) < 4:
        print("\t\t\t\t\tNO INPUT GRAPH or no. of cuts\n\n")
        sys.exit(0)

    fptr = open("final_" + sys.argv[1], 'a')
    fptr1 = open("final_comma_" + sys.argv[1], 'a')
    fptr1.write("W,CC,Variance,Peak_Temp\n")
    output= [0.0]*2
    graph = read_graph(sys.argv[1], sys.argv[3])
    print("read graph")
    # for i in range(8):
    #     for j in range(8):
    #         print(graph[i][j]," ")
    # print(graph)
    result_table = [0.0, 0.0]
    
    initialize_add()
    no_cuts = int(sys.argv[2])

    save_partition = [0] * no_cuts
    Header.seed_value = [0] * no_cuts

    for j in range(no_cuts):
        save_partition[j] = [0] * Graph_inf.No_nodes

    core_id = [0] * Graph_inf.No_nodes

    partition = [None, None]
    partition[0] = [0] * (Graph_inf.No_nodes // 2)
    partition[1] = [0] * (Graph_inf.No_nodes // 2)

    for j in range(Graph_inf.No_nodes):
        core_id[j] = j
        # print(core_id[j])

    flag = 0
    result_table[1] = 999999999
    i = 0
    flag = 0
    print("check")

    for k in range(NO_OF_RUN):
        flag = 0
        for j in range(no_cuts):
            Header.seed_value[j] = random.randint(0, 5147483647)
        # print(seed_value)
        perform_KL(sys.argv, graph, output)
        
        if result_table[1] > output[1]:
            flag = 1
        
        if flag == 1:
            result_table[0] = output[0]
            result_table[1] = output[1]

        print("\n\n\n\n\nfinished\n\n")

    fptr1.write(f"{result_table[0]},{result_table[1]}\n")
    fptr.close()
    fptr1.close()



def perform_KL(argv, netlist, output):
    t1 = time.process_time()
    
    core_id = None
    final_partition_core = None
    actual_no_of_nodes = nodes = 0

    st1 = "RESULTS628.txt"
    st2 = "KL2Dmap.txt"
    st3 = "KL2Dpir.txt"
    fp = open(st1, 'a')
    fp1 = open(st2, 'a')
    fp2 = open(st3, 'a')


    nodes=Graph_inf.No_nodes
    actual_no_of_nodes=Graph_inf.actual_No_nodes
    distri = int(sys.argv[3])
    core_id = [0] * nodes
    for i in range(nodes):
        core_id[i] = i
        # print(core_id[i])

    comm_cost = 0.0
    partition = [None, None]
    partition[0] = [0] * (nodes // 2)
    partition[1] = [0] * (nodes // 2) 
    init = int(sys.argv[2])
    
    final_partition_core = [0]*init
    for i in range(init):
        final_partition_core[i]=[0]*nodes
    rask = 0.0

    for i in range(init):
        Init_comm_cut_cost = 0
        Init_powbal = 0
        
        KL(i, netlist, core_id, nodes, partition)
        # print(core_id)
        # print(partition[0])
        # print(partition[1])
        # for i in range(4):
        #     print(partition[0][i] , partition[1][i])
        # print(final_partition_core)

        KL_partition(i, netlist, nodes//2, partition[0], final_partition_core)
        KL_partition(i, netlist, nodes//2, partition[1], final_partition_core)
        
        q.update(0)
        rask = cost(final_partition_core[i], netlist, nodes)
        # print(rask)
        for j in range(0, nodes, 2):
            fp.write(f"{final_partition_core[i][j]+1} {final_partition_core[i][j+1]+1}\t")
        
        fp.write(f"\n{i}\n{rask}\n\n")


    best_cost = float('inf')
    best = 0
    cost_f = [0.0] * init
    best_cost= 2147483647

    for i in range(init):
        print(i)
        cost_f[i] = map_nodes(nodes, final_partition_core[i], netlist)
    # print(cost_f)
    if distri == 1: 
        fp.write(f"\nDistributive\t{argv[1]}\tno. of cores= {actual_no_of_nodes}\tno. of cuts {init}\n")
        print(f"\nDistributive\t{argv[1]}\tno. of cores= {actual_no_of_nodes}\n")
    else:  
        fp.write(f"\n{argv[1]}\tno. of cores= {actual_no_of_nodes}\tno. of cuts {init}\n")
        print(f"\n{argv[1]}\tno. of cores= {actual_no_of_nodes}\n")
    
    for j in range(init):
        for i in range(0, nodes, 2):
            print(final_partition_core[j][i] + 1, final_partition_core[j][i + 1] + 1, "\t", end="")
            
            fp.write(f"{final_partition_core[j][i] + 1} {final_partition_core[j][i + 1] + 1}\t")

        cost_f[j] = cost(final_partition_core[j], netlist, nodes)
        temp = cost_f[j]
        
        if temp < best_cost:
            best_cost = temp
            best = j
        
        fp.write(f"\n{j}\n{cost_f[j]}\n\n")

    fp.write(f"\n\n***** best cost={float(cost_f[best])}\nbest ={best}")
    print("\n\n***** best cost=*****", cost_f[best])
    output[0] = cost(final_partition_core[best], netlist, nodes)
    print("\n cost in CC : ", output[0])
    output[1] = cost_f[best]
    print("\n\n\n*************\n", Graph_inf.No_nodes, "\t", Graph_inf.rows, "\t", Graph_inf.colums, "\n")
    t2 = time.process_time()

    fp1.write("\n\n" + argv[1] + "\n\n")
    fp2.write("\n\n" + argv[1] + "\n\n")

    corex = []
    inv_corex = []
    noedges = 0
    corex = [0] * nodes
    inv_corex = [0] * nodes
    for i in range(nodes):
        for j in range(i, nodes):
            if netlist[i][j] != 0 and netlist[i][j] != MAX:
                noedges += 1
    D = [Commodity() for _ in range(noedges)]
    tempx = Commodity()
    maxval = float('-inf')
    noedges = 0

    for i in range(nodes):
        for j in range(i, nodes):
            if netlist[i][j] != 0 and netlist[i][j] != MAX:
                D[noedges].value = netlist[i][j]
                D[noedges].source = i
                D[noedges].destination = j
                noedges += 1
    for i in range(noedges):
        for j in range(i, noedges):
            if D[i].value < D[j].value:
                tempx = D[i]
                D[i] = D[j]
                D[j] = tempx
    maxval = D[0].value
    pir = [0.0] * noedges

    for i in range(noedges):
        pir[i] = D[i].value / maxval
    for i in range(nodes):
        corex[address.row[i] * Graph_inf.colums + address.colum[i]] = final_partition_core[best][i]
    fp1.write("\nBest Cost = " + str(best_cost) + "\n")

    for i in range(nodes):
        inv_corex[corex[i]] = i
        fp1.write(str(i) + "\t" + str(corex[i]) + "\n")
    
    fp2.write("\n\nsrc-id\tdst-id\tpir\n")
    for i in range(noedges):
        fp2.write(f"{inv_corex[D[i].source]}\t{inv_corex[D[i].destination]}\t{pir[i]}\n")

    diff = (t2 - t1) # CLOCKS_PER_SEC

    fp.write(f"\tExecution Time: {diff}\n")
    print(f"\tExecution Time: {diff}\n")

    print("\n\n\n\n\nfinished\n\n")


def map_nodes(nodes, final_partition_core, graph):
    best_partition = 0
    temp_cost = 0.0
    
    temp_final_partition_core = [0] * nodes
    
    best_cost = [float('inf')] * 4
    Global_best = 0.0
    temp = 0.0
    
    iterative_improvement(graph, final_partition_core, nodes, 1)
    Final_Global_best_cost = cost(final_partition_core, graph, nodes)
    for i in range(nodes):
        temp_final_partition_core[i] = final_partition_core[i]
    
    iterative_improvement(graph, temp_final_partition_core, nodes, 0)
    best_cost[3] = cost(temp_final_partition_core, graph, nodes)
    best_cost[1]=best_cost[2]=best_cost[0]=MAX
    # print(best_cost)

    while True:
        iterative_improvement(graph, temp_final_partition_core, nodes, 0)
        # print("hello")
        temp = cost(temp_final_partition_core, graph, nodes)
        
        if temp <= best_cost[3]:
            best_cost[0] = best_cost[1]
            best_cost[1] = best_cost[2]
            best_cost[2] = best_cost[3]
            best_cost[3] = temp

        if temp == best_cost[3] and temp == best_cost[2] and temp == best_cost[1] and temp == best_cost[0]:
            break
    # print("hellp")       
    if Final_Global_best_cost > best_cost[3]:
        Final_Global_best_cost = best_cost[3]
        for i in range(nodes):
            final_partition_core[i] = temp_final_partition_core[i]

    Final_Global_best_cost = cost(final_partition_core, graph, nodes)

    return Final_Global_best_cost


def iterative_improvement(graph, final_partition_core, nodes, local):
    global a
    n4 = math.log(nodes) / math.log(2.0)
    n = int(n4)
    curr_lvl, t, w, min_row, max_row, min_col, max_col, shift, loop1, best_partition = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    best_cost = [0.0] * 4
    avg_row, avg_col, diffrence = 0.0, 0.0, 0.0
    i, j, k = 0, 0, 0
    level = int(math.log(nodes) / math.log(2.0)) - 1
    Global_best = 0.0

    temp_final_partition_core = [[0] * nodes for _ in range(4)]

    temp_col = [0] * nodes
    temp_row = [0] * nodes
    # print(temp_final_partition_core)
    for curr_lvl in range(level, 0, -1):
        for i in range(nodes):
            temp_final_partition_core[0][i] = temp_final_partition_core[1][i] = temp_final_partition_core[2][i] = temp_final_partition_core[3][i] = final_partition_core[i]

        for i in range(0, int(math.pow(2, curr_lvl)), 2):
            for j in range(nodes):
                temp_row[j] = address.row[j]
                temp_col[j] = address.colum[j]
            
            for k in range(nodes):
                if a[curr_lvl - 1][k] == i + 1:
                    break
            
            t = int(math.pow(2.0, n - curr_lvl))
            # print(t)
            min_row = address.row[k - t]
            min_col = address.colum[k - t]
            max_row = address.row[k - t]
            max_col = address.colum[k - t]

            for w in range(k - t, k):
                if address.row[w] > max_row:
                    max_row = address.row[w]

                if address.colum[w] > max_col:
                    max_col = address.colum[w]

            avg_row = (max_row + min_row) / 2.0
            avg_col = (max_col + min_col) / 2.0
            
            best_cost[0] = flip(graph, temp_final_partition_core[0], k, t, nodes, local)

            # print(best_cost)
            diffrence = (max_row - min_row) / 2.0
            shift = math.ceil(diffrence)

            for w in range(k - t, k):
                if address.row[w] >= avg_row:
                    address.row[w] = address.row[w] - shift
                elif address.row[w] < avg_row:
                    address.row[w] = address.row[w] + shift

            for w in range(nodes):
                for j in range(nodes):
                    if temp_row[w] == address.row[j] and temp_col[w] == address.colum[j]:
                        temp_final_partition_core[1][w] = final_partition_core[j]
                        break

            for j in range(nodes):
                address.row[j] = temp_row[j]
                address.colum[j] = temp_col[j]

            best_cost[1] = flip(graph, temp_final_partition_core[1], k, t, nodes, local)

            diffrence = (max_col - min_col) / 2.0
            shift = math.ceil(diffrence)

            for w in range(k - t, k):
                if address.colum[w] >= avg_col:
                    address.colum[w] = address.colum[w] - shift
                elif address.colum[w] < avg_col:
                    address.colum[w] = address.colum[w] + shift

            for w in range(nodes):
                for j in range(nodes):
                    if temp_row[w] == address.row[j] and temp_col[w] == address.colum[j]:
                        temp_final_partition_core[2][w] = final_partition_core[j]
                        break

            for j in range(nodes):
                address.row[j] = temp_row[j]
                address.colum[j] = temp_col[j]

            best_cost[2] = flip(graph, temp_final_partition_core[2], k, t, nodes, local)

            diffrence = (max_row - min_row) / 2.0
            shift = math.ceil(diffrence)

            for w in range(k - t, k):
                if address.row[w] >= avg_row:
                    address.row[w] = address.row[w] - shift
                elif address.row[w] < avg_row:
                    address.row[w] = address.row[w] + shift
    

            for w in range(nodes):
                for j in range(nodes):
                    if temp_row[w] == address.row[j] and temp_col[w] == address.colum[j]:
                        temp_final_partition_core[3][w] = final_partition_core[j]
                        break

            for j in range(nodes):
                address.row[j] = temp_row[j]
                address.colum[j] = temp_col[j]

            best_cost[3] = flip(graph, temp_final_partition_core[3], k, t, nodes, local)

            Global_best = best_cost[0]
            best_partition = 0

            for j in range(4):
                if Global_best > best_cost[j]:
                    Global_best = best_cost[j]
                    best_partition = j

            for j in range(nodes):
                final_partition_core[j] = temp_final_partition_core[best_partition][j]
    
    del temp_col
    del temp_row
    del temp_final_partition_core



def flip(G, final_partition_core, k, t, nodes, local):
    cost_arr = [0.0, 0.0, 0.0, 0.0]
    best_cost = 0.0
    avg_row = 0.0
    avg_col = 0.0
    diffrence = 0.0
    best = 0

    if local == 1:
        cost_arr[0] = best_cost = cost_local(final_partition_core, G, nodes, k - t, k + t)
    elif local == 0:
        cost_arr[0] = best_cost = cost(final_partition_core, G, nodes)

    temp_final_partition_core = np.zeros((4, nodes), dtype=int)
    temp_row = np.zeros(nodes, dtype=int)
    temp_col = np.zeros(nodes, dtype=int)

    for j in range(nodes):
        temp_row[j] = address.row[j]
        temp_col[j] = address.colum[j]
        temp_final_partition_core[0][j] = final_partition_core[j]

    min_row = address.row[k]
    min_col = address.colum[k]
    max_row = address.row[k]
    max_col = address.colum[k]
    # print(k , k+t , len(address.row))
    for w in range(k, k + t):
            if address.row[w] > max_row:
                max_row = address.row[w]

            if address.colum[w] > max_col:
                max_col = address.colum[w]


    avg_col = (max_col + min_col) / 2.0
    avg_row = (max_row + min_row) / 2.0

    # Flip along horizontal axis
    diffrence = (max_row - min_row) / 2.0
    shift = math.ceil(diffrence)
    for w in range(k, k + t):
            if address.row[w] >= avg_row:
                address.row[w] = address.row[w] - shift
            elif address.row[w] < avg_row:
                address.row[w] = address.row[w] + shift


    for w in range(nodes):
        for j in range(nodes):
            if temp_row[w] == address.row[j] and temp_col[w] == address.colum[j]:
                temp_final_partition_core[1][w] = final_partition_core[j]
                break

    for j in range(nodes):
        address.row[j] = temp_row[j]
        address.colum[j] = temp_col[j]

    if local == 1:
        cost_arr[1] = cost_local(temp_final_partition_core[1], G, nodes, k - t, k + t - 1)
    else:
        cost_arr[1] = cost(temp_final_partition_core[1], G, nodes)

    # Flip along vertical axis
    diffrence = (max_col - min_col) / 2.0
    shift = math.ceil(diffrence)
    for w in range(k, k + t):
            if address.colum[w] >= avg_col:
                address.colum[w] = address.colum[w] - shift
            elif address.colum[w] < avg_col:
                address.colum[w] = address.colum[w] + shift

    for w in range(nodes):
        for j in range(nodes):
            if temp_row[w] == address.row[j] and temp_col[w] == address.colum[j]:
                temp_final_partition_core[2][w] = final_partition_core[j]
                break

    for j in range(nodes):
        address.row[j] = temp_row[j]
        address.colum[j] = temp_col[j]

    if local == 1:
        cost_arr[2] = cost_local(temp_final_partition_core[2], G, nodes, k - t, k + t - 1)
    else:
        cost_arr[2] = cost(temp_final_partition_core[2], G, nodes)

    # Flip along horizontal axis
    diffrence = (max_row - min_row) / 2.0
    shift = math.ceil(diffrence)
    for w in range(k, k + t):    
        if address.row[w] >= avg_row:
            address.row[w] = address.row[w] - shift
        elif address.row[w] < avg_row:
            address.row[w] = address.row[w] + shift

    for w in range(nodes):
        for j in range(nodes):
            if temp_row[w] == address.row[j] and temp_col[w] == address.colum[j]:
                temp_final_partition_core[3][w] = final_partition_core[j]
                break

    for j in range(nodes):
        address.row[j] = temp_row[j]
        address.colum[j] = temp_col[j]

    if local == 1:
        cost_arr[3] = cost_local(temp_final_partition_core[3], G, nodes, k - t, k + t)
    else:
        cost_arr[3] = cost(temp_final_partition_core[3], G, nodes)

    # Finding the best partitioning
    for j in range(1,4):
        if(cost_arr[j]<best_cost):
            best_cost=cost_arr[j]
            best=j
				

    # Finalizing results
    for j in range(nodes):
        final_partition_core[j]=temp_final_partition_core[best][j]


    return best_cost



if __name__ == "__main__":
    main()
    