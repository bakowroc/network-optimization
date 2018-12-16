from Link import Link
from Node import Node


class Demand:
    def __init__(self, id, started_at, source: Node, destination: Node, bitrate, duration, slices):
        self.id = id
        self.started_at = started_at
        self.should_started_at = started_at
        self.source = source
        self.destination = destination
        self.bitrate = bitrate
        self.duration = duration
        self.slices = slices
        self.path = None

        self.allocated_links = []
        self.allocated_cores = []
        self.required_core = None
        self.cores_tried = []
        self.is_waiting = False
        self.is_success = False

    def allocate_or_else(self, current_iteration, path):
        if self.is_waiting:
            result= self.allocate_resources(path)
            if result:
                self.write_result(current_iteration)
                self.started_at = current_iteration
                print("[Demand {}]>> Started with delay {}".format(self.id, self.started_at - self.should_started_at))
                self.is_waiting = False
            else:
                self.wait()

        elif current_iteration == self.started_at:
            result = self.allocate_resources(path)
            if not result:
                self.wait()
            elif result:
                print("[Demand {}]>> Started normally".format(self.id))
                self.write_result(current_iteration)

        elif current_iteration == self.started_at + self.duration:
            print("\n[Demand {}]>> Finished".format(self.id))
            self.unallocate_resources()
            self.write_result(current_iteration)
            self.is_success = True
        else:
            self.write_result(current_iteration)


    def wait(self):
        print("[Demand {}]>> No resources available. Cleaning already allocated and waiting...".format(self.id))
        self.is_waiting = True
        self.unallocate_resources()

    def allocate_resources(self, path: [Link]):
        self.path = path
        print("\n[Demand {}]>> Allocating resources".format(self.id))
        for link in self.path:
            result, core = link.allocate_channel(self.id, self.slices, self.required_core)
            self.allocated_links.append(link.id)
            self.allocated_cores.append(core)
            if not result:
                return result
            elif self.required_core != core.id and self.required_core is not None:
                print("[Demand {}]>> Required core has changed".format(self.id))
                self.required_core = core.id
                self.unallocate_resources()
                result = self.allocate_resources(self.path)
                if result:
                    return result
            else:
                self.required_core = core.id

        return True

    def unallocate_resources(self):
        print("\n[Demand {}]>> Unallocating resources".format(self.id))
        for link in self.path:
            if link.id in self.allocated_links:
                link.unallocate_channel(self.id, self.slices, self.allocated_cores)

        self.allocated_links = []
        self.allocated_cores = []

    def write_result(self, iteration):
        for link in self.path:
            for core in link.cores:
                filename = "./data/{}/{}_{}_results.csv".format(link.id, link.id, core.id)
                _, taken_slices = core.get_slices_numbers()
                with open(filename, "a") as file:
                    file.write('{},{} \n'.format(iteration, taken_slices))
                    file.close()

