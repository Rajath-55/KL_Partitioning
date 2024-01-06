import math

def read_powerloss(powerloss,graph_number,Gr):
    file_name=f"opticalData/powerloss/cruxrouter/appGraph{graph_number}_loss.txt"
    print(file_name)
    try:
        with open(file_name,"r") as ptr:
            #print("hello",Gr.rows,Gr.colums)
            x=ptr.read()
            x=x.split("\t")
            #print(x)
            c=0
            for i in range(Gr.rows*Gr.colums):    
                for j in range(Gr.rows*Gr.colums):
                    powerloss[i][j]=float(x[c])
                    c+=1
        #print(powerloss)
    except FileNotFoundError:
        print("File not Found")
  

def evaluatePowerLoss(mapping,powerlossmatrix,Gr,edges):
    loss_wc=0
    inv_map=[0]*(Gr.nodes)
    for i in range(Gr.nodes):
        inv_map[mapping[i]]=i
    for i in range(Gr.edges):
        task_i=edges[i].destination
        task_j=edges[i].source
        mapp_core_task_i=inv_map[task_i]
        mapp_core_task_j=inv_map[task_j]
        loss=powerlossmatrix[mapp_core_task_i][mapp_core_task_j]
        if loss < loss_wc:
            loss_wc=loss
            sourcetaskwc=mapp_core_task_i
            destinationtaskwc=mapp_core_task_j
    return loss_wc


def read_validcomm(validcomm,graph_number,Gr):
    i,j,k,l=0,0,0,0
    file_name=f"opticalData/crosstalk/cruxrouter/appGraph{graph_number}_valid.txt"
    print(file_name)
    ptr=open(file_name,"r")
    if ptr is None:
        print("file can't be opened")
    x=ptr.read()
    x=x.split(" ")
    #print(x)
    c=0
    for i in range(Gr.rows*Gr.colums):
        for j in range(Gr.rows*Gr.colums):
            for k in range(Gr.rows*Gr.colums):
                for l in range(Gr.rows*Gr.colums):
                    if x[c][0]=="\n":
                       validcomm[i][j][k][l]=int(x[c][1])
                    elif x[c]!="\n":
                       validcomm[i][j][k][l]=int(x[c])            
                    c+=1
    ptr.close()



def read_crosstalk(crosstalk,graph_number,Gr):
    file_name=f"opticalData/crosstalk/cruxrouter/appGraph{graph_number}_crosstalk.txt"
    print(file_name)
    try:
        with open(file_name,"r") as ptr:
            x=ptr.read()
            x=x.split("\t")
            c=0
            for i in range(Gr.rows*Gr.colums):
                for j in range(Gr.rows*Gr.colums):
                    for k in range(Gr.rows*Gr.colums):
                        for l in range(Gr.rows*Gr.colums):
                            crosstalk[i][j][k][l]=float(x[c])
                            c+=1
    except FileNotFoundError:
        print("file can't be opened")


class crosstalkEdge:
  def __init__(self):
    self.src_noise_task=-1
    self.dst_noise_task=-1
    self.crosstalk=-1

def evaluateSNR(mapping,mapped_edges,powerlossmatrix,validcomm,crosstalk,SNR,srcTask,dstTask,Ploss,Crosstalk,Gr,edges):
    snrWC=9999 
    inv_map=[-1]*(Gr.rows*Gr.colums)
    crosstalkVar=0.0
    Tasklist=[crosstalkEdge() for _ in range(Gr.nodes)]

    for i in range(Gr.rows*Gr.colums):
        if mapping[i]!=-1:
            inv_map[mapping[i]]=i

    for i in range(Gr.edges):
        if mapped_edges[i]==1:
            ref_task_src=edges[i].source
            ref_task_dst=edges[i].destination

            for j in range(Gr.nodes):
                Tasklist[j].src_noise_task=-1
                Tasklist[j].dst_noise_task=-1
                Tasklist[j].crosstalk=-1

            task_noise_count=-1
            src_tile,dst_tile=-1,-1

            if inv_map[ref_task_src]!=-1 and inv_map[ref_task_dst]!=-1:
                src_tile=inv_map[ref_task_src]
                dst_tile=inv_map[ref_task_dst]
            else:
                continue

            powerloss=powerlossmatrix[src_tile][dst_tile]

            for j in range(Gr.edges):
                if i!=j and mapped_edges[j]==1:
                    noise_task_src=edges[j].source
                    noise_task_dst=edges[j].destination
                    noise_src_tile,noise_dst_tile=0,0

                    if inv_map[noise_task_src]!=-1 and inv_map[noise_task_dst]!=-1:
                        noise_src_tile=inv_map[noise_task_src]
                        noise_dst_tile=inv_map[noise_task_dst]
                    else:
                        continue

                    if validcomm[src_tile][dst_tile][noise_src_tile][noise_dst_tile]==1:
                        crosstalkVar=crosstalk[src_tile][dst_tile][noise_src_tile][noise_dst_tile]

                        if crosstalkVar==-1:
                            print("error in NoC architecture")

                        if crosstalkVar!=0:
                            task_noise_count+=1
                            Tasklist[task_noise_count].src_noise_task=noise_task_src
                            Tasklist[task_noise_count].dst_noise_task=noise_task_dst
                            Tasklist[task_noise_count].crosstalk=crosstalkVar

            crosstalkVar=0

            if task_noise_count>-1:
                sort_tasklist(Tasklist,task_noise_count+1)
                crosstalkVar=Tasklist[0].crosstalk

                for task_i in range(1,task_noise_count +1):
                    if Tasklist[task_i].src_noise_task!=-1 and Tasklist[task_i].dst_noise_task!=-1:
                        src_tile_i=inv_map[Tasklist[task_i].src_noise_task]
                        dst_tile_i=inv_map[Tasklist[task_i].dst_noise_task]
                        remove=False

                        for task_j in range(task_i):
                            if Tasklist[task_j].src_noise_task!=-1 and Tasklist[task_j].dst_noise_task!=-1:
                                src_tile_j=inv_map[Tasklist[task_j].src_noise_task]
                                dst_tile_j=inv_map[Tasklist[task_j].dst_noise_task]

                                if validcomm[src_tile_i][dst_tile_i][src_tile_j][dst_tile_j]==0:
                                    remove=True

                                if remove:
                                    Tasklist[task_i].src_noise_task=-1
                                    Tasklist[task_i].dst_noise_task=-1
                                    Tasklist[task_i].crosstalk=-1
                                else:
                                    crosstalkVar=sumDB(crosstalkVar,Tasklist[task_i].crosstalk)
            snr=calcSNR(powerloss,crosstalkVar)

            if snrWC>snr:
                snrWC=snr
                SNR=snr
                srcTask=ref_task_src
                dstTask=ref_task_dst
                Ploss=powerloss
                Crosstalk=crosstalkVar
    #print(SNR)
    return [SNR,srcTask,dstTask,Ploss,Crosstalk]

def sort_tasklist(tasklist,n):
  for i in range(n-1):
    for j in range(n-i-1):
      if tasklist[j].crosstalk<tasklist[j+1].crosstalk:
        temp=tasklist[j]
        tasklist[j]=tasklist[j+1]
        tasklist[j+1]=temp
  #return tasklist

def calcSNR(signal_attenuation,noise_attenuation):
  if noise_attenuation==0:
    return 9999
  return signal_attenuation - noise_attenuation

def sumDB(a,b):
  val_a=db_to_val(a)
  val_b=db_to_val(b)
  val_sum=val_a+val_b
  return val_to_db(val_sum)

def db_to_val(db):
  return 10**(db*0.1)

def val_to_db(val):
  return 10*math.log10(val)


