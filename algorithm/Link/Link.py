import os

from Core.Core import Core
from Node import Node


NUMBER_OF_CORES = 3

class Link:
    def __init__(self, start: Node, end: Node):
        self.id = start.name + end.name
        self.start = start
        self.end = end
        self.cores = self.create_cores()

        dir = './data/{}'.format(self.id)
        if not os.path.isdir(dir):
            os.mkdir(dir)

    def create_cores(self):
        cores = []
        for index in range(NUMBER_OF_CORES):
            name = str(self.start) + str(self.end)
            cores.append(Core(name, index + 1))

        return cores


    def allocate_channel(self, demand_id, demand_slices, required_core):
        print("--[Link {}]>> Allocating channel".format(self.id))
        needed_core = None
        if required_core is not None:
            needed_core = list(filter(lambda core: required_core == core.id, self.cores))[0]
            result = needed_core.update_slices(demand_id, demand_slices)
            if result:
                return result, needed_core

        cores = self.cores if needed_core is None else list(set(self.cores) - {needed_core})
        for core in cores:
            result = core.update_slices(demand_id, demand_slices)
            if result:
                return result, core

        print("--[Link {}]>> Failed to allocate channel".format(self.id))

        return False, None

    def unallocate_channel(self, demand_id, demand_slices, allocated_cores):
        print("--[Link {}]>> Freeing space in channel".format(self.id))
        self_cores = filter(lambda core: core in self.cores, allocated_cores)
        for core in self_cores:
            core.update_slices(demand_id, demand_slices, False)