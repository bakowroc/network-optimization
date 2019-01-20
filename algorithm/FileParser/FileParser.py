from Demand.Demand import Demand
from Link.Link import Link
from Node.Node import Node
from Path.Path import Path
from Topology.Topology import Topology


class FileParser:
    def __init__(self, entry_dir, demands_file, number_of_cores):
        self.entry_dir = entry_dir
        self.demands_file = demands_file
        self.number_of_cores = int(number_of_cores)
        self.topology = Topology()
        self.demands = []

        self.ffnet = {
            'name': 'ff.net',
            'number_of_nodes': 0,
            'number_of_links': 0
        }

        self.f30spec = {
            'name': 'f30.spec',
        }

        self.ff30pat = {
            'name': 'ff30.pat',
            'paths_chunks_number': 30,
            'number_of_paths': 0
        }

        demands_file_args = demands_file.split('_')
        self.dem = {
            'name': demands_file,
            'net_avg': demands_file_args[0],
            'block_number': demands_file_args[1]
        }

    def parse_ffnet(self):
        link_id = 0
        fname = self.entry_dir + self.ffnet['name']
        with open(fname) as f:
            content = f.readlines()
            self.ffnet['number_of_nodes'] = int(content[0])
            self.ffnet['number_of_links'] = int(content[1])

            for node_start_id, row in enumerate(content[2:]):
                path_lengths = list(map(lambda strval: int(strval), row.split('\t')))

                for node_end_id, path_len in enumerate(path_lengths):
                    if path_len is not 0:
                        node_start, node_end = self.get_ffnet_node(node_start_id, node_end_id)
                        link = Link(id=link_id, start=node_start, end=node_end, number_of_cores=self.number_of_cores, length=path_len)
                        self.topology.add_link(link)
                        link_id = link_id + 1

        self.ffnet_check()

    def get_ffnet_node(self, start_id, end_id):
        start_id_list = list(filter(lambda node: node.id == start_id, self.topology.nodes))
        if len(start_id_list) != 1:
            node_start = Node(start_id)
            self.topology.add_node(node_start)
        else:
            node_start = start_id_list[0]

        end_id_list = list(filter(lambda node: node.id == end_id, self.topology.nodes))
        if len(end_id_list) != 1:
            node_end = Node(end_id)
            self.topology.add_node(node_end)
        else:
            node_end = end_id_list[0]

        return node_start, node_end

    def parse_ff30spec(self) ->[[int]]:
        array_file = []
        fname = self.entry_dir + self.f30spec['name']
        with open(fname) as f:
            content = f.readlines()
            for row in content:
                spec_values = list(map(lambda strval: int(strval), row.replace(' \n', '').split(' ')))
                array_file.append(spec_values)

        return array_file

    def parse_ff30pat(self):
        spec = self.parse_ff30spec()
        curr_path_nr = 0
        fname = self.entry_dir + self.ff30pat['name']
        with open(fname) as f:
            content = f.readlines()
            self.ff30pat['number_of_paths'] = len(content)
            node_start = 0
            node_end = 1

            for line, row in enumerate(content):
                if curr_path_nr == self.ff30pat['paths_chunks_number']:
                    curr_path_nr = 0
                    if node_end == len(self.topology.nodes) - 1:
                        node_end = 1
                        node_start = node_start + 1
                    else:
                        node_end = node_end + 1

                path = Path(
                    curr_path_nr,
                    self.topology.get_node(node_start),
                    self.topology.get_node(node_end),
                    spec[line]
                )

                path_values = list(map(lambda strval: int(strval), row.split(' ')))

                for link_id, is_in_path_val in enumerate(path_values):
                    is_in_path = bool(int(is_in_path_val))
                    if is_in_path:
                        link = self.topology.get_link(link_id)
                        path.add_link(link)

                self.topology.add_path(path)
                curr_path_nr = curr_path_nr + 1

        self.ff30pat_check()

    def parse_dem(self):
        fname = self.entry_dir + self.dem['name']
        with open(fname) as f:
            content = f.readlines()

            for index, row in enumerate(content):
                demand_values = list(map(lambda strval: int(strval), row.split(' ')))
                demand = Demand(
                    id=index,
                    started_at=demand_values[0],
                    source=self.topology.get_node(demand_values[1]),
                    destination=self.topology.get_node(demand_values[2]),
                    bitrate=demand_values[3],
                    duration=demand_values[4]
                )
                self.demands.append(demand)

    def run(self) -> ([Demand], Topology):
        self.parse_ffnet()
        self.parse_ff30pat()
        self.parse_dem()

        return self.demands, self.topology, self.dem

    def ffnet_check(self):
        if self.ffnet['number_of_nodes'] != len(self.topology.nodes):
            print("File {} was parsed incorrectly: {}".format(self.ffnet['name'], "wrong number of nodes"))
            print("Was {}".format(len(self.topology.nodes)))
            print("Should be {}".format(self.ffnet['number_of_nodes']))
            exit(1)
        elif self.ffnet['number_of_links'] != len(self.topology.links):
            print("File {} was parsed incorrectly: {}".format(self.ffnet['name'], "wrong number of links"))
            print("Was {}".format(len(self.topology.links)))
            print("Should be {}".format(self.ffnet['number_of_links']))
            exit(1)

    def ff30pat_check(self):
        number_of_paths_chunk = len(list(filter(lambda path: path.nr == 29, self.topology.paths)))

        if self.ff30pat['number_of_paths'] != len(self.topology.paths):
            print("File {} was parsed incorrectly: {}".format(self.ff30pat['name'], "wrong number of paths"))
            print("Was {}".format(len(self.topology.paths)))
            print("Should be {}".format(self.ff30pat['number_of_paths']))
            exit(1)
        elif number_of_paths_chunk != self.ff30pat['number_of_paths'] / self.ff30pat['paths_chunks_number']:
            print("File {} was parsed incorrectly: {}".format(self.ff30pat['name'], "wrong number of path chunks"))
            exit(1)
