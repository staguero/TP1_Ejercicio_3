import random
import math
import copy
import time
import numpy as np

class SimulatedAnnealing():
    def __init__(self,stops_list,cost_list,temp_in):
        self.stops_list = stops_list
        self.cost_list = cost_list
        self.temp_in = temp_in
        self.it = 0
        self.temp = None
        self.current = None

    def start(self):
        random.seed(time.time())
        self.current = copy.deepcopy(self.stops_list)
        next = copy.deepcopy(self.current)
        best=copy.deepcopy(self.current)
        cost_best=self.path_cost(best)
        it=[]
        camino=[]
        probabilidad=[]
        temperatura=[]
        diferencias=[]

        while True: 
            self.temp = self.temp_in - self.it
            if self.temp <= 0:
                return [best, cost_best, it, camino, diferencias, probabilidad, temperatura] 
            permuts=random.sample(self.current,k=2)
            while 20000 in permuts:
                permuts=random.sample(self.current,k=2)
            aux=copy.deepcopy(next)
            for i in range(0,len(next)):
                if aux[i]==permuts[0]:
                    next[i]=permuts[1]

                if aux[i]==permuts[1]:
                    next[i]=permuts[0]
            cost_current = self.path_cost(self.current)
            cost_next = self.path_cost(next)
            dif = cost_next - cost_current
            try:
                expo = math.exp((self.temp_in-self.temp)/self.temp)
            except OverflowError:
                expo = float('inf')

            if dif < 0:
                self.current = copy.deepcopy(next)
                cost_current = cost_next
                if (cost_current < cost_best):
                    best=copy.deepcopy(self.current)
                    cost_best=cost_current
            else:
                prob = random.random()

                if prob < (1/expo):
                    self.current = copy.deepcopy(next)
                    cost_current = cost_next
                
            self.it = self.it + 1
            it.append(self.it)
            
            probabilidad.append(1/expo)
            temperatura.append(self.temp)
            diferencias.append(dif)

            next=copy.deepcopy(self.current)
            camino.append(cost_current)
            
    def path_cost(self,path):
        cost = 0
        count = 0
        while count < len(path)-1:
            for i in self.cost_list:
                if path[0+count] == i[0] and path[1+count] == i[1]: 
                    cost = cost + i[2]
                elif path[0+count] == i[1] and path[1+count] == i[0]:
                    cost = cost + i[2]
            count = count + 1
        return cost