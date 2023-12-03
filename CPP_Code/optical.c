#include "graph.h"
#include <stdio.h>
#include <stdlib.h>
extern struct graph_info Gr;
extern struct edge_info *edges;
void read_powerloss(double **powerloss, int graph_number)
{
   int i,j;
   FILE *ptr;
   /*powerloss = (double**)malloc(Gr.rows*Gr.colums*sizeof(double*));
   for(int i =0;i<Gr.rows*Gr.colums ;i++)
    {
        powerloss[i] = (double*)malloc(Gr.rows*Gr.colums *sizeof(double));
    }*/
    if(graph_number == 1)
    {
       ptr = fopen( "powerloss/cruxrouter/appGraph1_loss.txt","r");
    }
    else if (graph_number == 2)
    {
       ptr = fopen( "powerloss/cruxrouter/appGraph2_loss.txt","r");
    }
    else if (graph_number == 3)
    {
       ptr = fopen( "powerloss/cruxrouter/appGraph3_loss.txt","r");
    }
    else if (graph_number == 4)
    {
       ptr = fopen( "powerloss/cruxrouter/appGraph4_loss.txt","r");
    }
    else if (graph_number == 5)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph5_loss.txt","r");
    }
    else if (graph_number == 6)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph6_loss.txt","r");
    }
    else if (graph_number == 7)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph7_loss.txt","r");
    }
    else if (graph_number == 8)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph8_loss.txt","r");
    }
    else if (graph_number == 9)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph9_loss.txt","r");
    }
    else if (graph_number == 10)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph10_loss.txt","r");
    }
    else if (graph_number == 13)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph13_loss.txt","r");
    }
    else if (graph_number == 14)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph14_loss.txt","r");
    }
    else if (graph_number == 15)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph15_loss.txt","r");
    }
    else if (graph_number == 17)
    {
       ptr = fopen( "powerloss/cruxrouter/appGraph17_loss.txt","r");
    }
    else if (graph_number == 18)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph18_loss.txt","r");
    }
    else if (graph_number == 19)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph19_loss.txt","r");
    }
    else if (graph_number == 20)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph20_loss.txt","r");
    }
    else if (graph_number == 21)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph21_loss.txt","r");
    }
    else if (graph_number == 22)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph22_loss.txt","r");
    }
    else if (graph_number == 23)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph23_loss.txt","r");
    }
    else if (graph_number == 25)
    {
       ptr = fopen( "powerloss/cruxrouter/appGraph25_loss.txt","r");
    }
    else if (graph_number == 26)
    {
       ptr = fopen( "powerloss/cruxrouter/appGraph26_loss.txt","r");
    }
    else if (graph_number == 27)
    {
       ptr = fopen( "powerloss/cruxrouter/appGraph27_loss.txt","r");
    }
    else if (graph_number == 28)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph28_loss.txt","r");
    }
    else if (graph_number == 29)
    {
       ptr = fopen( "/home/sucharita/constructive_heuristics_optical/powerloss/cruxrouter/appGraph29_loss.txt","r");
    }
    else if (graph_number == 30)
    {
       ptr = fopen( "powerloss/cruxrouter/appGraph30_loss.txt","r");
    }
    
	if(ptr == NULL)
	{
	   printf("file can't be opened \n");
	  // return 1;
	        
	}
    for(i = 0; i<Gr.rows*Gr.colums; i++)
    {
        for(j = 0;j<Gr.rows*Gr.colums; j++)
           {    
               fscanf(ptr,"%lf\t",&powerloss[i][j]);

           }	
    }
    /*for(i = 0; i<Gr.rows*Gr.colums; i++)
    {
        for(j = 0;j<Gr.rows*Gr.colums; j++)
           {    
               printf("%lf",powerloss[i][j]);
           }	
           printf("\n");
    }*/

    fclose(ptr);
   // printf("sucharita");
}
double evaluatePowerLoss(unsigned short *mapping, double **powerlossmatrix)
{
    double loss,loss_wc = 0;//-999999;//-99999;//0;
    unsigned short *inv_map = new unsigned short [Gr.nodes];
    for(int i = 0;i<Gr.nodes;i++)
    {
      inv_map[mapping[i]] = i;
    }   
    for(int i = 0;i<Gr.edges;i++)
    {
      int task_i = edges[i].destination ;
      int task_j= edges[i].source ;
      
      int mapp_core_task_i = inv_map[task_i];
      int mapp_core_task_j = inv_map[task_j];
        //printf("sucharita samanta\n");
        //printf("%d\n", mapp_core_task_j);
       // printf("%d\n", mapp_core_task_i);
        /*for(int i = 0; i<Gr.rows*Gr.colums; i++)
         {
            for(int j = 0;j<Gr.rows*Gr.colums; j++)
             {    
               printf("%lf",powerlossmatrix[i][j]);
             }	
           printf("\n");
          }*/

      loss = powerlossmatrix[mapp_core_task_i][mapp_core_task_j];
      //printf("loss=%lf\n", loss);
                  //problem
     
        if (loss < loss_wc)//(loss < loss_wc)//(loss > loss_wc)   //loss < loss_wc
        {
            loss_wc = loss;
            int sourcetaskwc = mapp_core_task_i ;
            int destinationtaskwc = mapp_core_task_j;             
        }
     }
     //printf("loss_wc=%lf\n", loss_wc);
     //scanf("%d",&loss);
     return loss_wc;
                
}

