import os

from Core.Core import Core
from Demand import Demand
from Logger.Logger import Logger
from Node import Node

NUMBER_OF_CORES = 3


class Link:
    def __init__(self, id, start: Node, end: Node, length):
        self.id = id
        self.name = "L{}_{}".format(start.id, end.id)
        self.start = start
        self.end = end
        self.length = length
        self.cores = self.create_cores()

    def create_cores(self):
        cores = []
        for index in range(NUMBER_OF_CORES):
            name = "core_{}".format(str(self.start) + str(self.end))
            cores.append(Core(name, index))

        return cores

    def check_channel_availability(self, demand_slices: [int], required_core_id: int, required_start_index: int, already_checked: [int], already_checked_cores) -> (bool, int, Core):
        required_core = None

        def check_core(core_to_check):
            r, si = core_to_check.get_core_availability(demand_slices, required_start_index, already_checked)
            return r, si, core_to_check

        if required_core_id is not None:
            required_core = list(filter(lambda core: required_core_id == core.id, self.cores))[0]
            r, si, c = check_core(required_core)
            if r:
                return True, si, c

        cores = list(set(self.cores) - {required_core} - set(already_checked_cores))

        for core in cores:
            r, si, c = check_core(core)
            if r:
                return True, si, c

        return False, required_core_id, required_start_index

    def allocate_channel(self, demand: Demand):
        core = list(filter(lambda core: demand.required_core_id == core.id, self.cores))[0]
        core.allocate_for_demand(demand.id, demand.slices, demand.required_start_index)

    def unallocate_channel(self, demand: Demand):
        cores = filter(lambda core: core.id == demand.required_core_id, self.cores)
        for core in cores:
            core.unallocate_for_demand(demand.id, demand.slices)
