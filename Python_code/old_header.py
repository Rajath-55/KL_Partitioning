import sys
import os
import time
import math
import numpy as np
import random

MAX = 1000000
Lambda = 2
WEIGHT = 1.0

save_partition = None
seed_value = [0]*1000

q = 0

class virtual_address:
    def __init__(self):
        self.row = None
        self.colum = None

address = virtual_address()

Init_comm_cut_cost = 0
Init_powbal = 0
wt = WEIGHT
wt1 = WEIGHT
def partition_cost(graph, A, B, n):
    cut = 0.0
    for i in range(n):
        for j in range(n):
            cut += graph[A[i]][B[j]]

    # Uncomment the line below if you want to print the cut value
    # print(f"cut= {cut:.2f}")
    return cut

def Hops(snode, dnode, n):
    hop_count = abs(address.row[snode] - address.row[dnode]) + abs(address.colum[snode] - address.colum[dnode])
    return hop_count


def diff(first, second):
    dif = abs(first - second)
    return dif


def cost_cc(map, G, n):
    cost = 0.0
    for index1 in range(n):
        for index2 in range(index1 + 1, n):
            if G[map[index1]][map[index2]] != MAX and G[map[index1]][map[index2]] != 0:
                if G[map[index1]][map[index2]] == G[map[index2]][map[index1]]:
                    cost += (Hops(index1, index2, n) + 1) * 2 * G[map[index1]][map[index2]]
                else:
                    cost += (Hops(index1, index2, n) + 1) * 2 * G[map[index1]][map[index2]]
                    cost += (Hops(index1, index2, n) + 1) * 2 * G[map[index2]][map[index1]]
    return cost

def cost(map, G, n):
    cost = 0.0
    for index1 in range(n):
        for index2 in range(index1 + 1, n):
            if G[map[index1]][map[index2]] != MAX and G[map[index1]][map[index2]] != 0:
                if G[map[index1]][map[index2]] == G[map[index2]][map[index1]]:
                    cost += Hops(index1, index2, n) * G[map[index1]][map[index2]]
                else:
                    cost += Hops(index1, index2, n) * G[map[index1]][map[index2]]
                    cost += Hops(index2, index1, n) * G[map[index2]][map[index1]]
    return cost

def cost_local(map, G, n, start, end):
    cost = 0.0

    for index1 in range(start, end):
        for index2 in range(index1 + 1, end):
            if G[map[index1]][map[index2]] != MAX and G[map[index1]][map[index2]] != 0:
                if G[map[index1]][map[index2]] == G[map[index2]][map[index1]]:
                    cost += Hops(index1, index2, n) * G[map[index1]][map[index2]]
                else:
                    cost += Hops(index1, index2, n) * G[map[index1]][map[index2]]
                    cost += Hops(index1, index2, n) * G[map[index2]][map[index1]]
    return cost


def partition_cost(graph, A, B, n):
    cut = 0.0
    for i in range(n):
        for j in range(n):
            cut += graph[A[i]][B[j]]

    return cut

def KL(indx, graph, core_id, n, partition):
    random_partition(core_id, n,indx, partition)
    # print(core_id)
    temp_a = [0] * (n // 2)
    temp_b = [0] * (n // 2)

    Da = [0.0] * (n // 2)
    Db = [0.0] * (n // 2)
    Gain_k = [0.0] * (n // 2)
    Sum_Gain_k = [0.0] * (n // 2)

    temp_a = [partition[0][i] for i in range(n // 2)]
    temp_b = [partition[1][i] for i in range(n // 2)]


    counter = 0
    flag = 0
    old_max = float('inf')
    global Init_comm_cut_cost
    if Init_comm_cut_cost == 0:
        Init_comm_cut_cost = partition_cost(graph, temp_a, temp_b, n // 2)

    while True:
        counter = 0

        while counter<n//2:
            for j in range(counter, n // 2):
                Ia, Ib, Ea, Eb = 0.0, 0.0, 0.0, 0.0

                for i in range(n // 2):
                    Ia += graph[temp_a[j]][temp_a[i]]
                    Ea += graph[temp_a[j]][temp_b[i]]

                    Ib += graph[temp_b[j]][temp_b[i]]
                    Eb += graph[temp_b[j]][temp_a[i]]

                Da[j] = Ea - Ia
                Db[j] = Eb - Ib

            gain = -float('inf')


            for i in range(counter, n // 2):
                for j in range(counter, n // 2):
                    temp = (Da[i] + Db[j] - graph[temp_a[i]][temp_b[j]] - graph[temp_b[j]][temp_a[i]]) / Init_comm_cut_cost
                    if temp > gain:
                        gain = temp
                        I, J = i, j

            Gain_k[counter] = gain
            counter += 1
            swap_a, swap_b = temp_a[I], temp_b[J]

            for i in range(I, counter - 1, -1):
                temp_a[i] = temp_a[i - 1]

            temp_a[counter-1] = swap_b

            for i in range(J, counter - 1, -1):
                temp_b[i] = temp_b[i - 1]

            temp_b[counter-1] = swap_a

        for i in range(counter):
            Sum_Gain_k[i] = 0.0
            for j in range(i, -1, -1):
                Sum_Gain_k[i] += Gain_k[j]


        max = Sum_Gain_k[0]
        k = 0
        for i in range(counter):
            if Sum_Gain_k[i] > max:
                max = Sum_Gain_k[i]
                k = i

        for i in range(k + 1):
            for j in range(n // 2):
                if temp_b[i] == partition[0][j]:
                    partition[0][j] = temp_a[i]

                if temp_a[i] == partition[1][j]:
                    partition[1][j] = temp_b[i]

        temp_a = [partition[0][i] for i in range(n//2)]
        temp_b = [partition[1][i] for i in range(n//2)]


        if flag == 1:
            return

        if old_max <= max:
            flag = 1

        old_max = max

        if max < 0 or k >= (n // 2 - 1):
            break

    return

def random_partition(core_id, n, indx,partition):

    j = 0
    k = 0
    random.seed(seed_value[indx])

    for i in range(n):
        r = random.randint(0, 4294967296)
        # print(r)
        if r%2 == 0:
            if j < n // 2:
                partition[0][j] = core_id[i]
                j += 1
            else:
                partition[1][k] = core_id[i]
                k += 1
        else:
            if k < n // 2:
                partition[1][k] = core_id[i]
                k += 1
            else:
                partition[0][j] = core_id[i]
                j += 1


def KL_partition(indx, graph, n, core_id, final_partition_core):
    global q , Lambda
    if q>=8:
        q=0

    best_cost = 999999.0
    cut = 0.0

    if n <= Lambda:
        for i in range(Lambda):
            final_partition_core[indx][q]=(core_id[i])
            q+=1
        return
    # print(q)
    partition = [[0] * (n // 2) for _ in range(2)]
    best_partition = [[0] * (n // 2) for _ in range(2)]

    for i in range(n // 4):
        KL(indx, graph, core_id, n, partition)
        cut = partition_cost(graph, partition[0], partition[1], n // 2)
        if cut < best_cost:
            best_cost = cut
            for j in range(n // 2):
                best_partition[0][j] = partition[0][j]
                best_partition[1][j] = partition[1][j]

    del partition

    KL_partition(indx, graph, n // 2, best_partition[0], final_partition_core)
    KL_partition(indx, graph, n // 2, best_partition[1], final_partition_core)

    del best_partition
    return
