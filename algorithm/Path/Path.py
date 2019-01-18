from Node import Node


class Path:
    def __init__(self, nr, source: Node, destination: Node, spec):
        self.nr = nr
        self.name = "P{}_{}".format(source, destination)
        self.source = source
        self.destination = destination
        self.spec = self.create_spec(spec)
        self.links = []

    @staticmethod
    def round_nearest_spec(x, num=50):
        return int(round(float(x) / num) * num)

    @staticmethod
    def create_spec(spec):
        limit = 50
        spec_dict = {}
        for slice in spec:
            spec_dict[limit] = slice
            limit = limit + 50

        return spec_dict

    def add_link(self, link):
        self.links.append(link)

    def get_number_of_slices(self, bitrate):
        return self.spec[self.round_nearest_spec(bitrate)]

    def get_length(self):
        return sum(link.length for link in self.links)
