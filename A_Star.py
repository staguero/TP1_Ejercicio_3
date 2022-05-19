class A_Star():
    def __init__(self,mapa,current_node,target_node,cost=None):
        self.close_list=[]
        self.open_list=[]
        self.mapa = mapa
        self.current_node = current_node
        self.target_node = target_node
        self.path_cost = cost
        self.current_node.parent = self.current_node    #AGREGADO
    
    def in_close_list(self,node):
        if node in self.close_list:
            for value in self.close_list:
                if value.id == node.id:
                    return value
        else:
            return False
    
    def in_open_list(self,node):
        if node in self.open_list:
            return True
        else:
            return False

    def check_list(self,i,j,minF):
        try:
            if self.mapa[i][j].id[0:5] == "Shelf" or self.mapa[i][j].id[0:5] == "Bahía":
                if self.mapa[i][j].id == self.target_node.id: 
                    if minF.id != self.current_node.id:
                        self.mapa[i][j].parent = minF
                        self.close_list.append(self.mapa[i][j])
                        return
                    else:
                        return
                else:
                    return

            if self.in_close_list(self.mapa[i][j]):
                return

            auxG = minF.G + ( (minF.x-self.mapa[i][j].x)**2 + (minF.y-self.mapa[i][j].y)**2 ) **0.5
            auxH = ( (self.target_node.x-self.mapa[i][j].x)**2 + (self.target_node.y-self.mapa[i][j].y)**2 ) **0.5

            if self.in_open_list(self.mapa[i][j]):
                if (auxG + auxH) <= (self.mapa[i][j].G + self.mapa[i][j].H):
                    self.open_list.remove(self.mapa[i][j])
                    
                    self.mapa[i][j].parent = minF
                    self.mapa[i][j].G = auxG
                    self.mapa[i][j].H = auxH
                    self.open_list.append(self.mapa[i][j])
            else:
                self.mapa[i][j].parent = minF
                self.mapa[i][j].G = auxG
                self.mapa[i][j].H = auxH
                self.open_list.append(self.mapa[i][j])
        except:
            pass

    def min_F(self):
        minF = self.open_list[0]
        for node in self.open_list:
            if (node.G + node.H) <= (minF.G + minF.H):
                minF = node
        return minF
    
    def start_method(self,mapa_columnas,mapa_filas):
        path_list = []
        self.open_list.append(self.current_node)
        while True:
            tmp = self.in_close_list(self.target_node)
            if tmp:
                path_list = [[tmp.x, tmp.y]]
                try:
                    self.path_cost = tmp.parent.G + tmp.parent.H 
                except:
                    print("El nodo actual de error es:")
                    print(tmp.id)
                while tmp.id is not self.current_node.id:
                    tmp = tmp.parent
                    path_list.append([tmp.x, tmp.y])

                path_list.reverse()
                return path_list
            else:
                minF = self.min_F()

                self.close_list.append(minF)
                self.open_list.remove(minF)

                self.neighbor_check(minF,mapa_columnas,mapa_filas)


    def neighbor_check(self,minF,mapa_columnas,mapa_filas):
        for j in range(mapa_columnas):
            for i in range(mapa_filas):
                if self.mapa[i][j].x == minF.x:
                    if self.mapa[i][j].y == minF.y:
                            self.check_list(i+1,j,minF)
                            self.check_list(i+1,j-1,minF)
                            self.check_list(i+1,j+1,minF)
                            self.check_list(i-1,j,minF)
                            self.check_list(i-1,j-1,minF)
                            self.check_list(i-1,j+1,minF)
                            self.check_list(i,j-1,minF)
                            self.check_list(i,j+1,minF)

