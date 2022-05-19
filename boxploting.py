
# Import libraries
import matplotlib.pyplot as plt
import numpy as np

class boxploting():
    def __init__(self,data):
        self.data = data
        self.names=[]

    def start(self):
        for i, s in enumerate(self.data):
            a='P '+str(i+1)
            self.names.append(a)
        fig = plt.figure()
        boxprops = dict(linestyle='-', linewidth=1.5, color='#00145A')
        flierprops = dict(marker='o', markersize=6, linestyle='none')
        whiskerprops = dict(color='#00145A')
        capprops = dict(color='#00145A')
        medianprops = dict(linewidth=1.5, linestyle='-', color='#01FBEE')
        ba=plt.boxplot(self.data, labels=self.names, notch=False, boxprops=boxprops, whiskerprops=whiskerprops,capprops=capprops, flierprops=flierprops, medianprops=medianprops,showmeans=True)
        plt.show()