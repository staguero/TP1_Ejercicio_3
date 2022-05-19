def lector_ordenes():
    archivo=open('ordenes.txt',"r")
    lista_archivo=archivo.readlines()
    lista_final=[]
    posiciones = []
    for linea in lista_archivo:
        if "Order" in linea:
            posiciones.append(lista_archivo.index(linea))

    for k in range (len(posiciones)-1):
        lista_momentanea=[]
        for i in range(posiciones[k]+1,posiciones[k+1]-1):
            lista_archivo[i]=lista_archivo[i].replace("P","")
            lista_archivo[i]=lista_archivo[i].replace("\n","")
            lista_momentanea.append(lista_archivo[i])
        lista_final.append(lista_momentanea)

    lista_momentanea=[]
    for i in range(posiciones[len(posiciones)-1]+1,len(lista_archivo)):
        lista_archivo[i]=lista_archivo[i].replace("P","")
        lista_archivo[i]=lista_archivo[i].replace("\n","")
        lista_momentanea.append(lista_archivo[i])
    lista_final.append(lista_momentanea)

    return lista_final
