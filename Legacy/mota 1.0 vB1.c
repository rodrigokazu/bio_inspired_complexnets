#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

//Definições
//Número de neurônios
#define NN 10000
//SIN
#define SIN 500
//Número de sinapses
#define NC (SIN*NN)

#define PRINT_EACH 10000

//Alcance das sinapses ... 0 => infinito
#define SIN_RANGE 0

#define OUT 0
#define IN 1
#define INF (NN+1)

//Forçar feed forward?
#define FEED_FORWARD 1
//Preferential attachment?
#define PREFER 0
//Permitir arestas repetidas?
#define REPEAT_EDGES 1
//Imprimir arquivo com as arestas (pronto para o GraphPlot do Mathematica) - 0 = Não; 1 = Inicial/Final; 2 = A cada iteração; 3 = A cada deleção
#define WOLFRAM 0
//Ativar system ("pause") ?
#define PAUSE_AT_THE_END 1

#define DEBUG 0

//Protótipos
int add_edge(long,long,long);
double urand();
long krand();
void print_matrix_til(long);
void wolfram_print_matrix_til(long, char[]);
int included(long[],long,long);
int edge_exists(long,long);
long choose_weighted(long*,long);
long sum_of(long*,long);

//Variáveis
long conx[NC][2], indegs[NN], outdegs[NN], degs[NN], maxindeg = 0, maxoutdeg = 0, maxdeg = 0, it = 0;
int component[NN], giant, dfs_visited[NN],already_dead[NN];
char ts[64];

int main (int argc, char *argv[]) {
    long i,j,n1,n2,tki,to_kill[NN];
    int tries_of_n,fi,inf_flag;
    double asp;
    long node_to_kill, path_sum, path_total, smp,localmax,toll=0;
    char fn[256],sapp[16];
    FILE *f = NULL;
    time_t sT,mT,eT,tT;
    
    srand(time(NULL));
    
    //Zera o vetor de graus
    for (i=0;i<NN;i++) {
        indegs[i] = 0;
        outdegs[i] = 0;
        degs[i] = 1;
    }
    //Zera a matriz de conexões
    for (i=0;i<NC;i+=1) {
        conx[i][OUT] = 0;
        conx[i][IN] = 0;
    }
    printf("Começando ...\n");
    time(&sT);
    strftime(ts,64,"(%b %d, %Y - %Hh%M)",gmtime(&sT));
    //Processamento do modelo em si
    for (i=0;i<NC;i++) {
        if (i % 1000 == 0) printf("%ld / %ld\n",i,NC);
        
        if (PRINT_EACH && i % PRINT_EACH == 0) {
          fi = 0;
          for (j=1;j<NN;j++) {
          if (j < 50000 * fi) {
              fprintf(f,"%ld\n",indegs[j]+outdegs[j]);
          } else {
              if (f != NULL) fclose(f);
              sprintf(fn,"motaBATotalDeg%02d %s%s%sNN = %ld, added = %ld, SR = %ld, RT = %u.txt",fi,ts,PREFER ? " PA " : "",FEED_FORWARD ? " FF " : "",NN,i,100*SIN_RANGE/NN,clock()/CLOCKS_PER_SEC);
              fi ++;
              f = fopen(fn,"w");
              if (f == NULL) {
                  puts("Erro ao abrir arquivo.");
                  return 1;
              }
              fprintf(f,"%ld\n",indegs[j]+outdegs[j]);
           }
         }               
        }
        
         n1 = FEED_FORWARD ? krand() % (NN-2) + 1 : krand() % (NN-1) + 1;
         if (SIN_RANGE == 0) {
           if (PREFER) {
             n2 = FEED_FORWARD ? n1 + choose_weighted(&degs[n1+1],NN-n1-1) : choose_weighted(degs,NN);
           } else {
             n2 = FEED_FORWARD ? n1 + 1 + krand() % (NN-1-n1) : krand() % (NN-1) + 1;
           }
         } else {
           if (PREFER) {
             n2 = FEED_FORWARD ? n1 + choose_weighted(&degs[n1+1],(SIN_RANGE < NN-1-n1 ? SIN_RANGE : NN-1-n1)) : choose_weighted(degs,NN);
           } else {
             n2 = FEED_FORWARD ? n1 + 1 + krand() % (SIN_RANGE < NN-1-n1 ? SIN_RANGE : NN-1-n1) : krand() % (NN-1) + 1;
           }
         }
         add_edge(n1, n2, i);
     }
        
    time(&mT);
    fi = 0;
    for (j=1;j<NN;j++) {
        if (j < 50000 * fi) {
            fprintf(f,"%ld\n",indegs[j]+outdegs[j]);
        } else {
            if (f != NULL) fclose(f);
            sprintf(fn,"motaBAFinTotalDeg%02d %s%s%sNN = %ld, NC = %ld, SR = %ld, RT = %u.txt",fi,ts,PREFER ? " PA " : "",FEED_FORWARD ? " FF " : "",NN,NC,100*SIN_RANGE/NN,clock()/CLOCKS_PER_SEC);
            fi ++;
            f = fopen(fn,"w");
            if (f == NULL) {
                puts("Erro ao abrir arquivo.");
                return 1;
            }
            fprintf(f,"%ld\n",indegs[j]+outdegs[j]);
        }
    }
    time(&eT);
    
    printf("Começou em: ");
    printf(ctime(&sT));
    printf("\nTerminou de rodar: ");
    printf(ctime(&mT));
    printf("\nTerminou de escrever: ");
    printf(ctime(&eT));
    if (PAUSE_AT_THE_END) system("pause");
}

long choose_weighted(long *weights,long size) {
     long q = sum_of(weights,size);
//     printf("%ld %ld",*weights,size);
     long i = 0,r = krand() % q;
     while (r >= weights[i] && i < size) {
//         printf("r = %ld, weight %ld = %ld",r,i,weights[i]);
         r -= weights[i];
         i++;
     }
     return i;
}

long sum_of(long *vec,long size) {
     long sov = 0, i;
     for (i=0;i<size;i++) {
         sov += vec[i];
     }
     return sov;
}

//Checa se um vetor contém um elemento
int included(long list[],long size,long elem) {
    int i;
    for(i=0;i<size;i++) {
        if(list[i] == elem) {
            return 1;                   
        }
    }
    return 0;
}

//Checa se existe uma aresta entre dois vértices dados
int edge_exists(long a, long b) {
    long i;
    for (i=0;i<NC;i++) {
        if ((a == conx[i][OUT] && b == conx[i][IN]) || (b == conx[i][OUT] && a == conx[i][IN])) {
            return 1;
        }
    }
    return 0;    
}

//Adiciona uma aresta entre v1 e v2 na posição p
int add_edge(long v1, long v2, long p) {
    //if (v2 >= NN) return 1;
    //if (v1 == v2) return 1;
    //if (!(v1 && v2)) return 1;
    
    if (!REPEAT_EDGES) {
      long i;
      for (i=0;i<NC;i++) {
        if ((v1 == v2) || (conx[i][IN] == v2 && conx[i][OUT] == v1)) {
          return 0;
        }
      }
    }
    
    conx[p][OUT] = v1;
    conx[p][IN] = v2;
    
    outdegs[v1] ++;
    indegs[v2] ++;
    degs[v1] ++;
    degs[v2] ++;
    
/* Quando for usar o grau total descomentar as de baixo e comentar as de cima e quando não for, inverte */    
    
    if (outdegs[v1] > maxoutdeg) maxoutdeg = outdegs[v1];
    if (indegs[v2] > maxindeg) maxindeg = indegs[v2];
//    if (degs[v1] + degs[v1] > maxdeg) maxdeg = degs[v1];
//    if (degs[v2] + degs[v2] > maxdeg) maxdeg = degs[v2];

    return 0;
}

//Gera um número aleatório (a princípio) de 0 a 1073741823
//Usa a função rand() para funcionar => necessário incluir stdlib.h e chamar srand() antes de usar
long krand() {
    return (long) ((rand() % 32768) << 15) + (rand() % 32768);
}

//Retorna um número aleatório entre 0 e 1
double urand() {
    return (double) ((krand() % 10000000) / 10000000.0);
}

void print_matrix_til(long bottom) {
     long i;
     for(i=0;i<bottom;i++) {
         printf("[%ld %ld]\n",conx[i][OUT],conx[i][IN]);
     }
     system("pause");
}

void wolfram_print_matrix_til(long bottom, char appendix[16]) {
     long i;
     FILE *f = NULL;
     char fn[256];
     //sprintf(fn,"edgesMotaWolframTotalDegree %s NN = %ld, NC = %ld, A = %lf, r = %lf, IT %ld of %ld%s.txt",ts,NN,NC,PA,PR,it,ITS,appendix);
     f = fopen(fn,"w");
            if (f == NULL) {
                puts("Erro ao abrir arquivo.");
            }
            fprintf(f,"GraphPlot[{\n");
     for(i=0;i<bottom;i++) {
         if (i == bottom - 1)
           fprintf(f,"%ld -> %ld\n",conx[i][OUT],conx[i][IN]);
         else
           fprintf(f,"%ld -> %ld,\n",conx[i][OUT],conx[i][IN]);
     }
     //fprintf(f,"},VertexLabeling -> True]\n");
     fclose(f);
}
