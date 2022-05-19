from Node import *
import numpy as np

def crear_mapa(columnas_estante,estantes_f,estantes_c,individuo): #individuo es una elemento de la poblacion, es una lista 
    mapa_filas = 2*estantes_f+4+(estantes_f-1)*2
    mapa_columnas= estantes_c*columnas_estante+4+(estantes_c-1)*2
    mapa = [[Node(i,j,None) for j in range(mapa_columnas)] for i in range(mapa_filas)]

    for j in range(mapa_columnas):
        for i in range(mapa_filas):
            mapa[i][j].setID("Empty")

    #Asignacion de estantes y su nombre
    fin_columnas=mapa_columnas-(2+columnas_estante)
    m=np.linspace(2,fin_columnas,estantes_c)
    fin_filas=mapa_filas-(2+2)
    m2=np.linspace(2,fin_filas,estantes_f)
    valor=0
    for j in m:
        for i in m2:
            col=int(j)
            for k in range(columnas_estante): 
                mapa[int(i)][col].setID( "Shelf" + str(individuo[valor]) )
                mapa[int(i)+1][col].setID("Shelf" + str(individuo[valor+columnas_estante]) )
                col+=1
                valor+=1
            valor+=columnas_estante
    #Bahía de carga
    bahiacarga=20000
    mapa[0][0].setID("Bahia" + str(bahiacarga)) 
    return mapa