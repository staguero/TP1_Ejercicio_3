from copy import deepcopy
from itertools import combinations
from crear_mapa import *
from A_Star import *
from Simulated_Annealing import *
import random
import time 


class Genetic_Algorithm():
    def __init__(self,n_shelfs,n_individuals,orders):
        self.n_shelfs = n_shelfs
        self.n_individuals = n_individuals
        self.orders=orders

        self.population=[]

    def create_individual(self):
        random.seed(time.time())
        value = 1
        individual = [0] * self.n_shelfs
        while value <= self.n_shelfs:
            pos=random.randint(0,self.n_shelfs-1)
            if individual[pos]==0:
                individual[pos]=value
                value += 1
            else:
                other_pos=individual.index(0)
                individual[other_pos]=value
                value+=1
        return individual

    def create_population(self):
        while len(self.population) < self.n_individuals:
            self.population.append(self.create_individual())

    def fitness(self,map,mapa_filas,mapa_columnas):
        total_cost = 0
        for order in self.orders:
            stops_list=order
            cost_list = []
            count=0
            while count < len(stops_list):
                for value in range(count+1,len(stops_list)):
                    inicio=str(stops_list[count])
                    fin=str(stops_list[value])
                    for j in range(mapa_columnas):
                        for i in range(mapa_filas):
                            if map[i][j].id is not None:
                                if map[i][j].id[5:]==inicio:
                                    current_node = map[i][j]
                                if map[i][j].id[5:]==fin:
                                    target_node = map[i][j]
                    a_star = A_Star(map,current_node,target_node)
                    a_star.start_method(mapa_columnas,mapa_filas)

                    cost_list.append([inicio,fin,a_star.path_cost])
                count = count + 1

            temp=len(stops_list)*2000
            simulated_annealing = SimulatedAnnealing(stops_list,cost_list,temp) 
            lowcost_path = simulated_annealing.start()
            total_cost = lowcost_path[1] + total_cost
        return total_cost

    def selection(self,total_cost_list):
        random.seed(time.time())
        ordered_cost=sorted(total_cost_list)
        ordered_population=[]
        for i in ordered_cost:
            pos=total_cost_list.index(i)
            ordered_population.append(self.population[pos])

        probability=[]
        cost=0
        for i in range(int(len(ordered_cost)/2),len(ordered_cost)):
            cost=cost+ordered_cost[i]
            probability.append(cost)
        probability.insert(0,0)

        combinations_aux=[] 
        combinations = []
        for j in range(0,int(len(ordered_population)/2)): 
            count = 0
            while count < 2:
                indicator=random.uniform(0,max(probability))
                for k in range(0,len(probability)-1): 
                    if probability[k]<indicator<=probability[k+1]:
                        position=int(len(ordered_population)/2)+k
                        break

                if position not in combinations_aux:
                    combinations_aux.append(position)
                    count += 1

            combinations.append(combinations_aux[0])
            combinations.append(combinations_aux[1])
            combinations_aux.clear()

        return ordered_population,combinations

    def mutation(self,lista):
        random.seed(time.time())
        prob = random.random()
        if prob < 0.2:
            while True:
                pos1=random.randint(0,len(lista)-1)
                pos2=random.randint(0,len(lista)-1)
                if pos1==pos2:
                    pos2=random.randint(0,len(lista)-1)
                else:
                    break

            aux1=lista[pos1]
            aux2=lista[pos2]

            lista[pos1]=aux2
            lista[pos2]=aux1
        return lista
    
    def crossover(self,father_1,father_2):
        cut_point = random.randint(0,len(father_1)-2) #menos 2 para evitar que sea una copia igual al padre
        son_1 = deepcopy(father_2)
        for pos_f1,value_f1 in enumerate(father_1):
            if pos_f1 <= cut_point:
                pos_f2 = son_1.index(value_f1)
                son_1[pos_f2] = son_1[pos_f1]
                son_1[pos_f1] = value_f1

        son_2 = deepcopy(father_1)
        for pos_f2,value_f2 in enumerate(father_2):
            if pos_f2 <= cut_point:
                pos_f1 = son_2.index(value_f2)
                son_2[pos_f1] = son_2[pos_f2]
                son_2[pos_f2] = value_f2
        
        return son_1,son_2
    
    
    def generation(self,father,son,cut_1,cut_2):
        count_1=0
        for j in range(cut_2+1,self.n_shelfs): 
            if father[j] not in son[cut_1:cut_2+1]:
                son[j-count_1]=father[j]
                last_position=j-count_1
            else:
                count_1+=1
        pos_in=last_position+1        
        amount=self.n_shelfs-pos_in
        count_2=0

        for t in range(0,cut_2+amount):
            if father[t] not in son[cut_1:cut_2+1]:
                if pos_in <= self.n_shelfs-1:
                    son[pos_in]=father[t]
                    pos_in+=1
                else:
                    son[t-amount-count_2]=father[t]
            else:
                count_2+=1
    
        return son
        
    def start(self,n_it,columnas_estante,estantes_f,estantes_c):
        it = 0
        mapa_filas=2*estantes_f+4+(estantes_f-1)*2
        mapa_columnas=estantes_c*columnas_estante+4+(estantes_c-1)*2
        self.create_population()
        cost_min = 99999
        flag=0
        lista_fitness_population=[] #Guarda listas de Población y cada una tiene los [costos de cada mapa de población, , , ,]
        while it < n_it:
            total_cost_list = []
            lista_fitness_population.append([])
            for it2, individual in enumerate(self.population):
                map = crear_mapa(columnas_estante,estantes_f,estantes_c,individual)
                lista_fitness_population[it].append(self.fitness(map,mapa_filas,mapa_columnas))
                listaa=lista_fitness_population[it]
                total_cost_list.append(listaa[it2])
            s = sum(total_cost_list)
            if min(total_cost_list) < cost_min:
                cost_min = min(total_cost_list)
                flag=1
            print("Suma de costos de cada individuo (mapa) de la poblacion:")
            print(s)
            print("Individuo que ha tenido mejor costo hasta ahora: ")
            print(cost_min)
            print()

            for k in range(0,len(total_cost_list)):
                total_cost_list[k]=total_cost_list[k]/s
                total_cost_list[k]=(1/total_cost_list[k])/100

            ord_population,combinations=self.selection(total_cost_list) 
            new_population=[]

            if flag == 1:
                best_individual = ord_population[len(self.population)-1]
                flag = 0

            for t in range(0,int(len(combinations))-1,2):
                son_1,son_2=self.crossover(ord_population[combinations[t]],ord_population[combinations[t+1]])
                new_population.append(self.mutation(son_1))
                new_population.append(self.mutation(son_2))
            
            self.population.clear()
            self.population = new_population
            it += 1
        return best_individual, lista_fitness_population