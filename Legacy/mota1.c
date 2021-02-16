#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

//Definições
#define NN 12000
#define NC (20*NN)
#define PR (1.0/3.0)
#define PA 0.1
#define ITS 50
#define PRINT_EACH 1

#define OUT 0
#define IN 1

//Protótipos
long krand();

//Variáveis
long conx[NC][2], degrees[NN], maxdegree = 0, it = 0;

int main (int argc, char *argv[]) {
    long i,j,n1;
    double kp;
    char fn[16];
    FILE *f;
    srand(time(NULL));
    //Zera o vetor de graus
    for (i=0;i<NN;i+=1) {
        degrees[i] = 0;
    }
    //Itera ITS vezes
    for (it=0;it<ITS;it++) {
        //Gera conexões direcionadas do menor index para o maior index onde não houver conexões
        for (i=0;i<NC;i+=1) {
            if (!conx[i][OUT]) {
               n1 = krand() % NN;
               add_edge(n1, n1 + 1 + krand() % (NN-n1));
            }
        }
        //Mata neurônios preferencialmente
        for (j=0;j<NN;j+=1) {
            if (urand() <= kill_prob(j)) kill(j);            
        }
        //Se PRINT_EACH, imprime os graus -> nome do arquivo => motaOutput##.txt, ## é o número da iteração
        if (PRINT_EACH) {
            sprintf(fn,"motaOutput%d.txt",it);
            f = fopen(fn,"w");
            if (f == NULL) {
                puts("Erro ao abrir arquivo.");
                return 1;
            }
            
        }
    }
}

double kill_prob(long v) {
    double d = PA * (1-pow(degrees[v]/maxdegree,PR));
    return d;
}

//Retorna um número aleatório entre 0 e 1
double urand() {
    return (double) ((krand() % 10000000) / 10000000.0);
}

void kill(long v) {
     
}

int add_edge(long v1, long v2) {
    if (v1 == v2) return 0;
    if (!(v1 && v2)) return 0;
    
    //AQUI -> Efetivamente adiciona a aresta na matriz
    
    degrees[v1] ++;
    degrees[v2] ++;
    
    if (degrees[v1] > maxdegree) maxdegree = degrees[v1];
    if (degrees[v2] > maxdegree) maxdegree = degrees[v2];
}

//Gera um número aleatório (a princípio) de 0 a 1073741823
//Usa a função rand() para funcionar => necessário incluir stdlib.h e chamar srand() antes de usar

long krand() {
    return (long) ((rand() % 32768) << 15) + (rand() % 32768);
}
