import ctypes
import networkx as nx
import numpy as np
import os
import sys

class Tsp2dLib(object):

    def __init__(self, args):
        dir_path = os.path.dirname(os.path.realpath(__file__))        
        self.lib = ctypes.CDLL('%s/build/dll/libtsp2d.so' % dir_path)
        self.lib.Fit.restype = ctypes.c_double
        self.lib.Test.restype = ctypes.c_double
        self.lib.GetSol.restype = ctypes.c_double
        arr = (ctypes.c_char_p * len(args))()
        arr[:] = args
        self.lib.Init(len(args), arr)
        #print "python Init complete"
        self.ngraph_train = 0
        self.ngraph_test = 0

    def __CtypeNetworkX(self, g):
        coors = nx.get_node_attributes(g, 'pos')
        _demands = nx.get_node_attributes(g, 'demand')
        _depot = g.graph['depot']
        n = len(coors)+1#plus depot
        coor_x = (ctypes.c_double * n)()
        coor_y = (ctypes.c_double * n)()
        demands = (ctypes.c_double * n)()
        coor_x[0] = _depot[0]
        coor_y[0] = _depot[1]
        demands[0] = 1.0
        for i in range(1,n):
            coor_x[i], coor_y[i] = coors[i-1]
            demands[i] = _demands[i-1]
        return (n, ctypes.cast(coor_x, ctypes.c_void_p), ctypes.cast(coor_y, ctypes.c_void_p),
                ctypes.cast(demands,ctypes.c_void_p)) 

    def TakeSnapshot(self):
        self.lib.UpdateSnapshot()

    def ClearTrainGraphs(self):
        self.ngraph_train = 0
        self.lib.ClearTrainGraphs()

    def InsertGraph(self, g, is_test):
        n_nodes, coor_x, coor_y,demands = self.__CtypeNetworkX(g)
        if is_test:
            t = self.ngraph_test
            self.ngraph_test += 1
        else:
            t = self.ngraph_train
            self.ngraph_train += 1

        self.lib.InsertGraph(is_test, t, n_nodes, coor_x, coor_y, demands)
    
    def LoadModel(self, path_to_model):
        p = ctypes.cast(path_to_model, ctypes.c_char_p)
        self.lib.LoadModel(p)

    def SaveModel(self, path_to_model):
        p = ctypes.cast(path_to_model, ctypes.c_char_p)
        self.lib.SaveModel(p)

    def GetSol(self, gid, maxn):
        sol = (ctypes.c_int * (maxn + 20))()
        val = self.lib.GetSol(gid, sol)
        return val, sol

if __name__ == '__main__':
    f = Tsp2dLib(sys.argv)
