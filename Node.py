class Node():
    def __init__(self,x,y,parent_node):
        self.id = None
        self.G = 0
        self.H = 0
        self.x=x
        self.y=y
        self.parent=parent_node

    def setID(self,identificacion):
        self.id=identificacion