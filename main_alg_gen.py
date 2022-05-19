from Genetic_Algorithm import *
from lector_ordenes import *
from boxploting import *

def dibujo():
    for i in range(mapa_filas):
        print(mapa_dibujo[i])

columnas_estante=2
estantes_f=5
estantes_c=5
mapa_filas = 2*estantes_f+4+(estantes_f-1)*2
mapa_columnas= estantes_c*columnas_estante+4+(estantes_c-1)*2

orders = lector_ordenes()
for i in orders:
    i.insert(0,20000)
    i.append(20000)

n_shelfs = columnas_estante*2*estantes_c*estantes_f
n_individuals = 6
n_iteraciones = 20
object=Genetic_Algorithm(n_shelfs,n_individuals,orders)
best_individual, lista_fitness_population = object.start(n_iteraciones,columnas_estante,estantes_f,estantes_c)
print("Mejor individuo")
print(best_individual)
mapa=crear_mapa(columnas_estante,estantes_f,estantes_c,best_individual)
print()
print()
mapa_dibujo=[]
mapa_dibujo = [[0 for j in range(mapa_columnas)] for i in range(mapa_filas)]
for j in range(mapa_columnas):
        for i in range(mapa_filas):
            if mapa[i][j].id == "Empty":
                mapa_dibujo[i][j]="0 "
            else:
                mapa_dibujo[i][j]=mapa[i][j].id[5:]
dibujo()
bp=boxploting(lista_fitness_population)
bp.start()
input()