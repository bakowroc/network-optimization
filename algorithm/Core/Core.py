class Core:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.slices = [0] * 320
        self.indexes = {}

    def update_slices(self, demand_id, demand_slices, is_allocating = True):
        if is_allocating:
            if not self.is_going_to_be_full(demand_slices):
                self.allocate_for_demand(demand_id, demand_slices)
                return True
            print("----[Core {}]>> Core is full. Cannot allocate".format(self.id))
            return False
        else:
            self.unallocate_for_demand(demand_id, demand_slices)
            return True

    def allocate_for_demand(self, demand_id, demand_slices):
        print("----[Core {}]>> Allocated slices".format(self.id))
        self.indexes[demand_id] = len(self.slices) - 1
        for index, slice in enumerate(demand_slices * [1]):
            self.slices.insert(self.indexes[demand_id] + index, slice)

    def unallocate_for_demand(self, demand_id, demand_slices):
        print("----[Core {}]>> Unallocated slices".format(self.id ))
        start_index = self.indexes[demand_id]
        self.indexes.pop(demand_id)
        for index, slice in enumerate(demand_slices * [0]):
            self.slices[start_index + index] = slice


    def get_slices_numbers(self):
        empty_slices = len(list(filter(lambda slice: slice == 0, self.slices)))
        taken_slices = len(self.slices) - empty_slices

        return empty_slices, taken_slices

    def is_going_to_be_full(self, demand_slices):
        _, taken_slices = self.get_slices_numbers()
        return taken_slices + demand_slices > 320