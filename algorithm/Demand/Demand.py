from Logger.Logger import Logger
from Node import Node
from Path import Path


class Demand:
    def __init__(self, id, started_at, source: Node, destination: Node, bitrate, duration):
        self.id = id
        self.started_at = started_at
        self.source = source
        self.destination = destination
        self.bitrate = bitrate
        self.duration = duration
        self.slices = 0
        self.path = None

        self.required_core_id = None
        self.required_start_index = None
        self.already_checked_indexes = []
        self.already_checked_cores = []

        self.is_success = False

    def calculate_slices(self):
        self.slices = self.path.get_number_of_slices(self.bitrate)

    def mark_as_failed(self):
        self.is_success = False
        self.write_csv()

    def check_and_allocate(self, current_iteration, path: Path):
        self.path = path
        self.calculate_slices()

        if current_iteration == self.started_at:
            result = self.check_resources()
            if not result:
                return False

            self.allocate_resources()
            self.is_success = True
        elif current_iteration == self.started_at + self.duration:
            self.write_csv()
            self.unallocate_resources()

        return True

    def check_resources(self) -> bool:
        checked_links = 0

        for link in self.path.links:
            result, start_index, core = link.check_channel_availability(
                self.slices,
                self.required_core_id,
                self.required_start_index,
                self.already_checked_indexes,
                self.already_checked_cores,
            )

            if not result:
                return False

            if self.required_core_id is None:
                self.required_core_id = core.id
            elif self.required_core_id != core.id:
                self.already_checked_indexes = []
                self.already_checked_cores.append(core)
                self.required_core_id = core.id
                break

            if self.required_start_index is None:
                self.required_start_index = start_index
            elif self.required_start_index != start_index:
                self.already_checked_indexes.append(self.required_start_index)
                self.required_start_index = start_index
                break

            checked_links = checked_links + 1

        if checked_links != len(self.path.links):
            self.check_resources()

        return True

    def allocate_resources(self):
        for link in self.path.links:
            link.allocate_channel(self)

    def unallocate_resources(self):
        for link in self.path.links:
            link.unallocate_channel(self)

    def write_csv(self):
        filename = "./demands_summary.csv"
        if self.path:
            link_in_path = list(map(lambda link: link.id, self.path.links))
            path_length = self.path.get_length() or [],
        else:
            link_in_path = None
            path_length = None

        with open(filename, "a") as file:
            file.write('{}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}\n'.format(
                self.id,
                self.started_at,
                self.source.id,
                self.destination.id,
                self.bitrate,
                self.duration,
                self.is_success,
                link_in_path,
                path_length,
                self.required_core_id,
                self.required_start_index
            ))
            file.close()
