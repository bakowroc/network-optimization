import os

from Core.Core import Core
from Demand import Demand
from Logger.Logger import Logger
from Node import Node

class Link:
    def __init__(self, id, start: Node, end: Node, number_of_cores, length):
        self.id = id
        self.name = "L{}_{}".format(start.id, end.id)
        self.start = start
        self.end = end
        self.length = length
        self.cores = self.create_cores(number_of_cores)

    def create_cores(self, number_of_cores):
        cores = []
        for index in range(number_of_cores):
            name = "core_{}_{}".format(index, self.name)
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
                return r, si, c

        available_cores = list(set(self.cores) - {required_core} - set(already_checked_cores))
        if len(available_cores) > 0:
            for core in available_cores:
                r, si, c = check_core(core)
                if r:
                    return r, si, c

        return False, None, None

    def allocate_channel(self, demand: Demand):
        core = list(filter(lambda core: demand.required_core_id == core.id, self.cores))[0]
        core.allocate_for_demand(demand.slices, demand.required_start_index)

    def unallocate_channel(self, demand: Demand):
        core = list(filter(lambda core: core.id == demand.required_core_id, self.cores))[0]
        core.unallocate_for_demand(demand.slices, demand.required_start_index)
