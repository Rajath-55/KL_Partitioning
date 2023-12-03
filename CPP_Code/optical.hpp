#ifndef optical_h
#define optical_h

void read_powerloss(double **powerloss, int graph_number);
double evaluatePowerLoss(unsigned short *mapping, double **powerlossmatrix);
#endif
