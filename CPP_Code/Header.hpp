#ifndef Header_h
#define Header_h

#include "fstream"
#include "iostream"
#include <assert.h>
#include <limits.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

using namespace std;

#define MAX 1000000
#define Lambda 2 //// Define value for smallest partitions size.
#define WEIGHT 1.0
extern int **save_partition;
extern int *seed_value;
/***************** Global variables***************************/
unsigned short q = 0;
struct virtual_address {
  int *row, *colum;
} address;

double Init_comm_cut_cost = 0, Init_powbal = 0, wt = WEIGHT, wt1 = WEIGHT;

/*************************************************************/

/*********************** Function declaration ******************/
void random_partition(int *core_id, int n, int indx, int **partition);
void KL(int indx, double **graph, int *core_id, int n, int **partition);
double partition_cost(double **graph, int *A, int *B, int n);
// double partition_cost_power(double *core_pow, int *A, int *B, int n);
void KL_partition(int indx, double **graph, int n, int *core_id,
                  int *final_partition_core);
double flip(double **G, int *final_partition_core, int k, int t, int nodes,
            int local);
void iterative_improvement(double **G, int *final_partition_core, int nodes,
                           int local);
double diff(unsigned short, unsigned short);
unsigned short int Hops(unsigned short, unsigned short, int);
void print_graph(double **graph);
void print_arr(int **arr, int num_nodes, int num_cols);
/**************************************************************/

/* Function KL_partition() */
/*Inputs: n => number of nodes in the graph */
/*		  final_partition_core => array holding the final core sequence
 * generated after partitioning */
/*		  graph => adjacency matrix */
/*		  core_id => array containing the initial sequence of cores */
/*		  core_pow => array containing power values of each core */

/*Output: final_partition_core => array holding the final core sequence
 * generated after partitioning */

/* Description : This function is the control function for KL() partitioning
 * function. It recursively calls itself till the smallest partition size is
 * reached. The smallest size of partition is controlled by 'lambda' which is
 * '2' for MoT and Mesh and '4' for BFT. It takes a number of random cuts for
 * each partition by calling KL() and calculates the cut cost. The partitioning
 * with the best cut cost is accepted and passed for further partitioning*/

void KL_partition(int indx, double **graph, int n, int *core_id,
                  int *final_partition_core) {
  int i, j;
  double best_cost = INT_MAX, cut;

  // printf("q : %d\n", q);

  if (n <= Lambda) //// Lambda = 2 for MoT and Mesh, while Lambda = 4 for BFT
  {                //// Lambda represents the smallest partitions size.
    for (i = 0; i < Lambda; i++) {
      final_partition_core[q++] = core_id[i];
    }

    return;
  }
  int **partition, **best_partition;

  partition = (int **)malloc(2 * sizeof(int *));
  partition[0] = (int *)malloc(n / 2 * sizeof(int));
  partition[1] = (int *)malloc(n / 2 * sizeof(int));

  best_partition = (int **)malloc(2 * sizeof(int *));
  best_partition[0] = (int *)malloc(n / 2 * sizeof(int));
  best_partition[1] = (int *)malloc(n / 2 * sizeof(int));

  for (i = 0; i < n / 4; i++) //// number of random cuts reduced to n/4. It can
                              /// be changed according to
                              /// requirement
  {
    // srand(i);
    KL(indx, graph, core_id, n, partition);

    cut = partition_cost(graph, partition[0], partition[1], n / 2);
    // printf("CUT : %f\n", cut);
    if (cut < best_cost) {
      best_cost = cut;
      for (j = 0; j < n / 2; j++) {
        best_partition[0][j] = partition[0][j];
        best_partition[1][j] = partition[1][j];
      }
    }
  }
  // printf("PARTITION : ");
  // print_arr(partition, 2, n / 2);
  // printf("BEST PARITITON : ");
  // print_arr(best_partition, 2, n / 2);
  // printf("FINAL PARTITION CORE : ");
  free(partition);
  // printf("\nbest cost=%0.2f\n",best_cost);

  KL_partition(indx, graph, n / 2, best_partition[0], final_partition_core);
  KL_partition(indx, graph, n / 2, best_partition[1], final_partition_core);
  free(best_partition);
  return;
}

/* Function random_partition() */
/*Inputs: n => number of nodes in the graph */
/*		  partition => 2D array holding the 2 partitions generated */
/*		  core_id => array containing the initial sequence of cores */

/*Output: partition => 2D array holding the 2 partitions generated */

/* Description : This function randomly bi-partitions the core sequence passed
 * to it.*/

void random_partition(int *core_id, int n, int indx, int **partition) {
  int i, j, k, r;

  j = 0;
  k = 0;
  assert(!(n & 1));
  // for (int i = 0; i < n; ++i) {
  //   if (i < n / 2)
  //     partition[0][j++] = core_id[i];
  //   else
  //     partition[1][k++] = core_id[i];
  // }
  // printf("\n");
  // j = k = 0;
  // for (int i = 0; i < n; ++i) {
  //   if (i % 2 == 0) {
  //     printf("%d", partition[0][j++]);
  //   } else {
  //     printf(" %d\n", partition[1][k++]);
  //   }
  // }
  // printf("\n\n\n");
  // return

      srand(seed_value[indx]);
  for (i = 0; i < n; i++) {
    r = rand();

    if ((r % 2) == 0) {
      if (j < n / 2) {
        partition[0][j] = core_id[i];
        j++;
      } else {
        partition[1][k] = core_id[i];
        k++;
      }
    } else {
      if (k < n / 2) {
        partition[1][k] = core_id[i];
        k++;
      } else {
        partition[0][j] = core_id[i];
        j++;
      }
    }
  }

  /*int i,j,k,r;

  j=0;
  k=0;

  for (i=0;i<n/2;i++)
   {
          partition[0][j] = save_partition[indx][i];
          partition[1][j] = save_partition[indx][n/2+i];
          printf(" %d,
  %d,",save_partition[indx][i],save_partition[indx][n/2+i]); j++;
   }
   printf("\n\n");*/
}

/* Function KL_partition() */
/*Inputs: n => number of nodes in the graph */
/*		  partition => 2D array holding the 2 partitions generated by KL
 * algorithm */
/*		  graph => adjacency matrix */
/*		  core_id => array containing the initial sequence of cores */
/*		  core_pow => array containing power values of each core */

/*Output: partition => 2D array holding the 2 partitions generated by KL
 * algorithm */

/* Description : This function is the implementation of the KL bi-patitioning
 * algorithm. Firstly, it calls random_partition() to generate 2 random
 * partitions and then performs swapping according to KL algorithm. The
 * partitions thus generated are returned.*/

void KL(int indx, double **graph, int *core_id, int n, int **partition) {
  int i, j, k, r;

  // FILE *fp;
  // fp=fopen("partition.txt","a");

  random_partition(core_id, n, indx, partition);
  /*---------------------------partition generation done Code for KL
   * partitioning needs a & b array & graph------------*/

  int *temp_a, *temp_b, counter, I, J, swap_a, swap_b;
  double Ia, Ib, Ea, Eb, Pow_a, Pow_b, *Da, *Db, gain, temp, *Gain_k,
      *Sum_Gain_k, max;

  temp_a = (int *)malloc(n / 2 * sizeof(int));
  temp_b = (int *)malloc(n / 2 * sizeof(int));

  Da = (double *)malloc(n / 2 * sizeof(double));
  Db = (double *)malloc(n / 2 * sizeof(double));

  Gain_k = (double *)malloc(n / 2 * sizeof(double));
  Sum_Gain_k = (double *)malloc(n / 2 * sizeof(double));

  for (i = 0; i < n / 2; i++) {
    temp_a[i] = partition[0][i];
    temp_b[i] = partition[1][i];
  }

  int flag = 0;
  double old_max = INT_MAX;

  if (Init_comm_cut_cost == 0) {
    Init_comm_cut_cost = partition_cost(graph, temp_a, temp_b, n / 2);
  }

  // cout<<"\nInit_comm"<<Init_comm_cut_cost<<"\nInit_powbal"<<Init_powbal<<endl;

  do {
    counter = 0; ////unlocking all nodes for next iteration
    /*for(i=0;i<n/2;i++)
    {
            Pow_a+=core_pow[temp_a[i]];
            Pow_b+=core_pow[temp_b[i]];
    }*/

    while (counter < n / 2) {

      for (j = counter; j < n / 2; j++) {
        Ia = 0.0;
        Ea = 0.0;
        // Pow_a=0.0;					/////clearing Ia Ib Ea
        // Eb

        Ib = 0.0;
        Eb = 0.0;
        // Pow_b=0.0;

        for (i = 0; i < n / 2; i++) {
          Ia += graph[temp_a[j]][temp_a[i]]; /// J th element vs rest in a and b
          Ea += graph[temp_a[j]][temp_b[i]];
          // Pow_a+=core_pow[temp_a[i]];

          Ib += graph[temp_b[j]][temp_b[i]];
          Eb += graph[temp_b[j]][temp_a[i]];
          // Pow_b+=core_pow[temp_b[i]];
        }
        Da[j] = Ea - Ia; // gain of moving element j from partition a to b
        Db[j] = Eb - Ib; // gain of moving element j from partition b to a
        // norm_powbal=fabs(Pow_a-Pow_b)/Init_powbal;

        // fprintf(fp,"\nj=%d Da=%f Db=%f Ea=%f Eb=%f Ia=%f
        // Ib=%f",j,Da[j],Db[j],Ea,Eb,Ia,Ib);
      }

      gain = -1.0 * INT_MAX; // consider gain negative also

      for (i = counter; i < n / 2; i++) {
        for (j = counter; j < n / 2; j++) {

          temp = (Da[i] + Db[j] - graph[temp_a[i]][temp_b[j]] -
                  graph[temp_b[j]][temp_a[i]]) /
                 Init_comm_cut_cost; ///////Cost calculation
          ///////************think about it*************//////////
          if (temp > gain) {
            gain = temp;
            I = i;
            J = j;
          }
          // fprintf(fp,"\ni=%d j=%d temp=%f graph[ai][bj]=%f
          // graph[bj][ai]=%f",i,j,temp,graph[temp_a[i]][temp_b[j]],graph[temp_b[j]][temp_a[i]]);
        }
      }

      Gain_k[counter++] = gain;
      swap_a = temp_a[I];
      swap_b = temp_b[J];
      // fprintf(fp,"\nGainK=%f\n",Gain_k[counter-1]);

      for (i = I; i >= counter; i--) {
        // swap=temp_a[I];
        temp_a[i] = temp_a[i - 1];
        // temp_b[J]=swap;
      }
      temp_a[counter - 1] = swap_b;

      for (i = J; i >= counter; i--) {
        // swap=temp_a[I];
        temp_b[i] = temp_b[i - 1];
        // temp_b[J]=swap;
      }
      temp_b[counter - 1] = swap_a;
    }

    for (i = 0; i < counter; i++) {
      Sum_Gain_k[i] = 0.0;
      for (j = i; j >= 0; j--) {
        Sum_Gain_k[i] += Gain_k[j];
      }
    }

    /*----------Finding k such that sum of Gain is maximised ----------*/
    max = Sum_Gain_k[0];
    k = 0;
    for (i = 0; i < counter; i++) {
      if (Sum_Gain_k[i] > max) {
        max = Sum_Gain_k[i];
        k = i;
      }
    }

    /************Finalizing partitions****************/ // changing the actual
                                                        // partition.

    for (i = 0; i <= k; i++) {
      for (j = 0; j < n / 2; j++) {
        if (temp_b[i] == partition[0][j]) {
          partition[0][j] = temp_a[i];
        }

        if (temp_a[i] == partition[1][j]) {
          partition[1][j] = temp_b[i];
        }
      }
    }

    for (i = 0; i < n / 2; i++) {
      temp_a[i] = partition[0][i];
      temp_b[i] = partition[1][i];
    }
    if (flag == 1) {
      free(temp_a);
      free(temp_b);
      free(Gain_k);
      free(Sum_Gain_k);
      free(Da);
      free(Db);
      return;
    }

    if (old_max <= max) {
      flag = 1;
    }
    old_max = max;

  } while (max >= 0 &&
           k < (n / 2 - 1)); // repeating the process till there can be no more
                             // gain i.e., the gain max becomes negative.

  free(temp_a);
  free(temp_b);
  free(Gain_k);
  free(Sum_Gain_k);
  free(Da);
  free(Db);
  return;
}

/* Function partition_cost() */
/*Inputs: n => number of nodes in the graph */
/*		  graph => adjacency matrix */
/*		  A => holds the cores present in partition A */
/*		  B => holds the cores present in partition B */

/*Output: cut cost or the cost of inter-communication between partition A and B
 */

/* Description : This function calculates the cut cost between partition A and
 * B*/

double partition_cost(double **graph, int *A, int *B, int n) {
  double cut = 0.0;
  int i, j;
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
      cut += graph[A[i]][B[j]];
    }
  }

  // printf("cut= %0.2f\n",cut);
  return cut;
}

/******************** For Mesh ***********************/

/* Function cost_local() */
/*Inputs: n => number of nodes in the graph */
/*		  G => adjacency matrix */
/*		  start => starting index of partition under consideration*/
/*		  end => end index of the partition under consideration */
/*		  map => suquence of cores*/
/*Output: local communication cost (in Hops x Bandwidth) */

/* Description : This function calculates the local communication cost (in Hops
 * x Bandwidth) of a partition*/

double cost_local(int *map, double **G, int n, int start, int end) {
  unsigned short index1, index2;
  double cost = 0;
  for (index1 = start; index1 < end; index1++) {
    for (index2 = index1 + 1; index2 < end; index2++) {
      if (G[map[index1]][map[index2]] != MAX &&
          G[map[index1]][map[index2]] != 0) {
        if (G[map[index1]][map[index2]] == G[map[index2]][map[index1]]) {
          cost = cost +
                 (double)Hops(index1, index2, n) * G[map[index1]][map[index2]];
        }

        else {
          cost = cost +
                 (double)Hops(index1, index2, n) * G[map[index1]][map[index2]];
          cost = cost +
                 (double)Hops(index1, index2, n) * G[map[index2]][map[index1]];
        }
      }
    }
  }
  // printf("In cost local : cost = %.6f\n", cost);
  return cost;
}

/* Function cost() */
/*Inputs: n => number of nodes in the graph */
/*		  G => adjacency matrix */
/*		  map => suquence of cores*/
/*Output: communication cost (in Hops x Bandwidth) of the whole network*/

/* Description : This function calculates the total communication cost (in Hops
 * x Bandwidth) of the network */

double cost(int *map, double **G, int n) {
  unsigned short index1, index2;
  double cost = 0;
  for (index1 = 0; index1 < n; index1++) {
    for (index2 = index1 + 1; index2 < n; index2++) {
      if (G[map[index1]][map[index2]] != MAX &&
          G[map[index1]][map[index2]] != 0) {
        if (G[map[index1]][map[index2]] == G[map[index2]][map[index1]]) {
          cost = cost +
                 (double)Hops(index1, index2, n) * G[map[index1]][map[index2]];
        }

        else {
          cost = cost +
                 (double)Hops(index1, index2, n) * G[map[index1]][map[index2]];
          cost = cost +
                 (double)Hops(index2, index1, n) * G[map[index2]][map[index1]];
        }
      }
    }
  }
  // printf("In cost global : cost = %.6f\n", cost);
  return cost;
}

/* Function cost_cc() */
/*Inputs: n => number of nodes in the graph */
/*		  G => adjacency matrix */
/*		  map => suquence of cores*/
/*Output: communication cost (in Router cycles x Bandwidth) of the whole
 * network*/

/* Description : This function calculates the total communication cost (in
 * Router cycles x Bandwidth) of the network */

double cost_cc(int *map, double **G, int n) {
  unsigned short index1, index2;
  double cost = 0;
  for (index1 = 0; index1 < n; index1++) {
    for (index2 = index1 + 1; index2 < n; index2++) {
      if (G[map[index1]][map[index2]] != MAX &&
          G[map[index1]][map[index2]] != 0) {
        if (G[map[index1]][map[index2]] == G[map[index2]][map[index1]]) {
          cost = cost + (double)(Hops(index1, index2, n) + 1) * 2 *
                            G[map[index1]][map[index2]];
        }

        else {
          cost =
              cost +
              (double)(Hops(index1, index2, n) + 1) * 2 *
                  G[map[index1]][map[index2]]; ////Router cycles are taken as 2
          cost = cost + (double)(Hops(index1, index2, n) + 1) * 2 *
                            G[map[index2]][map[index1]];
        }
      }
    }
  }
  return cost;
}

/* Function Hops() */
/*Inputs: n => number of nodes in the graph */
/*		  node1 => starting node*/
/*		  node2 => Destination node*/
/*Output: hop_count => noumber of hops between node1 and node2*/

/* Description : This function calculates the total Hops required to reach node2
 * starting from node1 */

unsigned short int Hops(unsigned short snode, unsigned short dnode, int n) {
  unsigned short int hop_count;
  hop_count = abs(address.row[snode] - address.row[dnode]) +
              abs(address.colum[snode] - address.colum[dnode]);
  // printf("Hop Count : %d\n", hop_count);
  return hop_count;
}

double diff(unsigned short first, unsigned short second) {
  double dif;
  dif = abs(first - second);
  return dif;
}

void print_graph(double **graph, int num_nodes) {
  int i = 0, j = 0;

  for (int i = 0; i < num_nodes; ++i) {
    for (int j = 0; j < num_nodes; ++j) {
      cout << graph[i][j] << " ";
    }
    cout << "\n";
  }
}

void print_arr(int **graph, int num_nodes, int num_cols) {

  int i = 0, j = 0;

  for (int i = 0; i < num_nodes; ++i) {
    for (int j = 0; j < num_cols; ++j) {
      cout << graph[i][j] << " ";
    }
    cout << "\n";
  }
}
#endif
