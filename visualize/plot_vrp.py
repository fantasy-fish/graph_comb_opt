#!/usr/bin/env python

import csv
import sys
import pickle
import pprint
import matplotlib
import numpy as np

matplotlib.use('agg')

from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

assert len(sys.argv) > 1, "Missing test ID"
pp = pprint.PrettyPrinter(indent=4)

ID = sys.argv[1]
TESTFILE = "test-vrp-"+str(int(ID)+1)+"-"+str(int(ID)+1)+"-gnn-51-51.csv"
VALIDSET = "../data/vrp/validation/vrp"+str(ID)+".pkl"


# Gives us the rainbow color
def discrete_cmap(N, base_cmap=None):
    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)

# Plot the routes
def plot_vehicle_routes(ax, capacity=0.0, coords={}, demands={}, depot=[],
                        tour=[], tour_length=0.0, tour_size='0', tour_w=0):

    ax.plot(depot[0], depot[1], 'sk', markersize=20)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    legend = ax.legend(loc='upper center')

    routes = []
    for node in tour:
        if node == '0':
            routes.append([])
        else:
            routes[-1].append(int(node))

    cmap = discrete_cmap(len(routes) + 2, 'nipy_spectral')
    dem_rects = []
    used_rects = []
    cap_rects = []
    qvs = []
    total_dist = 0

    for veh_number, r in enumerate(routes):
        color = cmap(len(routes) - veh_number)

        r_demands = [ demands[x] for x in r ]
        r_coords = [ tuple(coords[x]) for x in r ]

        xs = [ c[0] for c in r_coords ]
        ys = [ c[1] for c in r_coords ]

        if sum(r_demands) > capacity:
            print('WARNING: Route Demands exceed Capacity!!!')

        ax.plot(xs, ys, 'o', mfc=color, markersize=5, markeredgewidth=0.0)

        dist = 0
        x_prev, y_prev = tuple(depot)
        cum_demand =0

        for (x, y), d in zip(r_coords, r_demands):
            dist += np.sqrt((x - x_prev)**2 + (y - y_prev)**2)

            cap_rects.append(Rectangle((x,y), 0.01, 0.1))
            used_rects.append(Rectangle((x,y), 0.01, 0.1*sum(r_demands)/capacity))
            dem_rects.append(Rectangle((x,y + 0.1*cum_demand/capacity), 0.01, 0.1*d/capacity))

            x__prev, y_prev = x, y
            cum_demand += d

        dist += np.sqrt((depot[0] - x_prev)**2 + (depot[1] - y_prev)**2)
        total_dist += dist
        qv = ax.quiver(
                xs[:-1],
                ys[:-1],
                np.array(xs[1:]) - np.array(xs[:-1]),
                np.array(ys[1:]) - np.array(ys[:-1]),
                scale_units='xy',
                angles='xy',
                scale=1,
                color=color,
                label='R {}, # {}, c {} / {}, d {:.2f}'.format(
                        veh_number,
                        len(r),
                        int(sum(r_demands)),
                        capacity,
                        dist))

        qvs.append(qv)
    ax.set_title('DQN-S2V: {} routes, total distance {:.2f}'.format(
            len(routes), total_dist))
    ax.legend(handles=qvs)

    pc_cap = PatchCollection(cap_rects, facecolor='whitesmoke', alpha=1.0,
            edgecolor='lightgray')
    pc_used = PatchCollection(used_rects, facecolor='lightgrey', alpha=1.0,
            edgecolor='lightgray')
    pc_dem = PatchCollection(dem_rects, facecolor='black', alpha=1.0,
            edgecolor='black')

    visualize_demands = False
    if visualize_demands:
        ax.add_collection(pc_cap)
        ax.add_collection(pc_used)
        ax.add_collection(pc_dem)


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


    for i, r in enumerate(results):
        pp.pprint(r)
        fig, ax = plt.subplots(figsize=(10,10))
        plot_vehicle_routes(ax, **r)
        fig.savefig("./images/cvrp_{}.png".format(i))
        plt.close()


if __name__ == "__main__":
    plot_vrp()
