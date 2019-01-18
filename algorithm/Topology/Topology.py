from Link import Link
from Logger.Logger import Logger
from Node import Node
from Path import Path


class Topology:
    def __init__(self):
        self.links = []
        self.nodes = []
        self.paths = []

    def add_link(self, link: Link):
        self.links.append(link)

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_path(self, path: Path):
        self.paths.append(path)

    def get_link(self, link_id) -> Link:
        link = list(filter(lambda link: link.id == link_id, self.links))
        if len(link) != 1:
            Logger.print("Cannot get link {}".format(link_id))
            exit(1)
        else:
            return link[0]

    def get_node(self, node_id) -> Node:
        node = list(filter(lambda node: node.id == node_id, self.nodes))
        if len(node) != 1:
            Logger.print("Cannot get link {}".format(node_id))
            exit(1)
        else:
            return node[0]

    def get_paths(self, start, end) -> [Path]:
        paths = list(filter(lambda path: path.source.id == start and path.destination.id == end, self.paths))
        if len(paths) == 0:
            Logger.print("Cannot get path for {} -> {}".format(str(start), str(end)))
            return []
        else:
            return self.sort_paths_by_len(paths)

    @staticmethod
    def sort_paths_by_len(paths):
        return sorted(paths, key=lambda path: path.get_length(), reverse=False)

