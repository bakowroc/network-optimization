## Nodes
import shutil

from Demand.Demand import Demand
from Link.Link import Link
from Node.Node import Node
import os
import numpy as np
import matplotlib.pyplot as plt

## Consts
TOTAL_DURATION = 320
PROCEED = True

if PROCEED:
    dir = './data'
    if not os.path.isdir(dir):
        os.mkdir(dir)
    else:
        shutil.rmtree(dir)

nodeA = Node("A")
nodeB = Node("B")
nodeC = Node("C")
nodeD = Node("D")
nodeE = Node("E")
nodeF = Node("F")

## Links

linkAB = Link(start = nodeA, end = nodeB)
linkBD = Link(start = nodeB, end = nodeD)
linkDC = Link(start = nodeD, end = nodeC)
linkCA = Link(start = nodeC, end = nodeA)
linkCE = Link(start = nodeC, end = nodeE)
linkEF = Link(start = nodeE, end = nodeF)
linkFD = Link(start = nodeF, end = nodeD)

## Paths
pathAB = [linkCA, linkDC, linkBD]
pathEF = [linkCE, linkDC, linkFD]

paths = {
    "AB": pathAB,
    "BA": pathAB,
    "EF": pathEF,
    "FE": pathEF
}

## Demands
demandEF = Demand(1, 0, nodeE, nodeF, bitrate = 1, duration= 125, slices = 120)
demandAB = Demand(2, 1, nodeA, nodeB, bitrate = 1, duration= 110, slices = 300)
demandFE = Demand(3, 2, nodeF, nodeE, bitrate = 1, duration= 32, slices = 210)
demandBA = Demand(4, 3, nodeB, nodeA, bitrate = 1, duration= 151, slices = 265)

def show_chart(link: Link):
    legend = []
    for core in link.cores:
        filename = './data/{}/{}_{}_results.csv'.format(link.id, link.id, core.id)
        data = np.genfromtxt(filename, delimiter=',', names=['iteration', 'slices'])
        legend.append("Core {}".format(core.id))
        plt.plot(data['iteration'], data['slices'],  linewidth=2)

    plt.legend(legend)
    plt.title("Link {}".format(link.id))
    plt.show(block=True)

def get_path(source: Node, destination: Node):
    return paths[source.name + destination.name]

def main():
    iteration = 0
    demands = [demandAB, demandEF, demandFE, demandBA]

    while(iteration <= TOTAL_DURATION and PROCEED):
        demands_starting_now = list(filter(lambda demand: demand.started_at <= iteration, demands))
        demands_finishing_now= list(filter(lambda demand: demand.started_at + demand.duration == iteration, demands))
        prepared_demands = set(demands_finishing_now + demands_starting_now)

        for demand in prepared_demands:
            path = get_path(demand.source, demand.destination)
            demand.allocate_or_else(iteration, path)
        iteration= iteration + 1

    for link in pathAB + pathEF:
        show_chart(link)




if __name__ == "__main__":
    main()