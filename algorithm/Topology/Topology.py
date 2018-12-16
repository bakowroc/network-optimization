from Link import Link
from Node import Node


class Topology:
    def __init__(self, nodes: [Node], links: [Link]):
        self.nodes = nodes
        self.links = links
