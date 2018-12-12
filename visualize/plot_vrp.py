#!/usr/bin/env python

import csv
import sys
import pickle
import pprint
import matplotlib

matplotlib.use('agg')

from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D


pp = pprint.PrettyPrinter(indent=4)

TESTFILE = "test-vrp-11-11-gnn-51-51.csv" 
VALIDSET = "vrp10.pkl"


def plot_vehicle_routes(ax, capacity=0.0, coords={}, demands={}, depot=[],
                        tour=[], tour_length=0.0, tour_size='0', tour_w=0):

    ax.plot(depot[0], depot[1], 'sk', markersize=20)


def plot_vrp():

    results = []

    with open(TESTFILE, 'r') as f:
        tours = csv.reader(f, delimiter=',')
        for t in tours:
            results.append({})
            results[-1]['tour_length'] = float(t[0])
            results[-1]['tour'] = t[1].split(' ')[1:]
            results[-1]['tour_size'] = t[1].split(' ')[0]
            results[-1]['tour_w'] = t[2]

    i = 0
    with open(VALIDSET, 'r') as f:
        dataset = pickle.load(f)
        for data in dataset:
            depot, coords, demands, capacity = data
            results[i]['depot'] = depot
            results[i]['coords'] = dict(zip(range(1,1+len(coords)),coords))
            results[i]['demands'] = dict(zip(range(1,1+len(demands)),demands))
            results[i]['capacity'] = capacity
            i += 1

    pp.pprint(results)

    for i, r in enumerate(results):
        fig, ax = plt.subplots(figsize=(10,10))
        plot_vehicle_routes(ax, **r)
        fig.savefig("./images/cvrp_{}.png".format(i))
        plt.close()
        break


if __name__ == "__main__":
    plot_vrp()
