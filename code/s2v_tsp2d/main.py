import numpy as np
import networkx as nx
import cPickle as cp
import random
import ctypes
import os
import sys
from tqdm import tqdm
import pickle

sys.path.append( '%s/tsp2d_lib' % os.path.dirname(os.path.realpath(__file__)) )
from tsp2d_lib import Tsp2dLib

n_valid = 100

def find_model_file(opt):
    '''
    max_n = int(opt['max_n'])
    min_n = int(opt['min_n'])
    log_file = None
    if max_n < 100:
        return None
    if min_n == 100 and max_n == 200:
        n1 = 50
        n2 = 100
    else:
        n1 = min_n - 100
        n2 = max_n - 100
    '''
    n = int(opt['max_n'])-1
    log_file = '%s/log-%d.txt' % (opt['save_dir'], n)
    if not os.path.isfile(log_file):
        return None
    best_r = 1000000
    best_it = -1
    with open(log_file, 'r') as f:
        for line in f:
            if 'average' in line:
                line = line.split(' ')
                it = int(line[1].strip())
                r = float(line[-1].strip())
                if r < best_r:
                    best_r = r
                    best_it = it
    if best_it < 0:
        return None
    return '%s/nrange_iter_%d.model' % (opt['save_dir'], n, best_it)

def PrepareGraphs(isValid):
    if isValid:
        n_graphs = 100
        prefix = 'validation'
    else:
        n_graphs = 10000
        prefix = 'train'
    n_nodes = int(opt['max_n'])-1
    filename = '%s/%s/vrp%d.pkl' % (opt['data_root'], prefix, n_nodes )

    with open(filename, 'r') as f:
        dataset = pickle.load(f)
        for data in dataset:
            depot,_coors,_demands,capacity = data
            n_nodes = len(_coors)
            assert n_nodes == len(_demands)
            coors = dict(zip(range(n_nodes),_coors))
            _demands = [1.0*d/capacity for d in _demands]
            demands = dict(zip(range(n_nodes),_demands))
            g = nx.Graph()
            g.add_nodes_from(range(n_nodes))
            nx.set_node_attributes(g, 'pos', coors)
            nx.set_node_attributes(g, 'demand', demands)
            g.graph['depot'] = depot
            api.InsertGraph(g, is_test=isValid)
        

if __name__ == '__main__':
    api = Tsp2dLib(sys.argv)
    print "Initialization complete"

    opt = {}
    for i in range(1, len(sys.argv), 2):
        opt[sys.argv[i][1:]] = sys.argv[i + 1]

    model_file = find_model_file(opt)
    if model_file is not None:
        print 'loading', model_file
        sys.stdout.flush()
        api.LoadModel(model_file)

    PrepareGraphs(isValid=True)
    PrepareGraphs(isValid=False)
    print "PrepareGraphs complete"

    # startup    
    for i in range(10):
        api.lib.PlayGame(100, ctypes.c_double(1.0))
    api.TakeSnapshot()

    eps_start = 1.0
    eps_end = 1.0

    eps_step = 10000.0
    api.lib.SetSign(1)

    lr = float(opt['learning_rate'])
    for iter in range(int(opt['max_iter'])):
        eps = eps_end + max(0., (eps_start - eps_end) * (eps_step - iter) / eps_step)
        if iter % 10 == 0:
            api.lib.PlayGame(10, ctypes.c_double(eps))

        if iter % 100 == 0:
            frac = 0.0
            for idx in range(n_valid):
                frac += api.lib.Test(idx)
            print 'iter', iter, 'lr', lr, 'eps', eps, 'average tour length: ', frac / n_valid
            sys.stdout.flush()
            model_path = '%s/nrange_%d_%d_iter_%d.model' % (opt['save_dir'], int(opt['min_n']), int(opt['max_n']), iter)
            api.SaveModel(model_path)

        if iter % 1000 == 0:
            api.TakeSnapshot()
            lr = lr * 0.95

        api.lib.Fit(ctypes.c_double(lr))
