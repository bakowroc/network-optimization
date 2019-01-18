class Core:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.slices = [0] * 320
        self.indexes = {}

    def get_core_availability(self, demand_slices: [int], required_start_index: int, already_checked: [int]) -> (bool, int):
        has_space, start_index = self.check_or_get_slices_space(demand_slices, required_start_index, already_checked)
        if has_space:
            return True, start_index

        return False, required_start_index

    def check_or_get_slices_space(self, demand_slices, required_start_index, already_checked) -> (bool, int):
        if required_start_index is not None:
            start_index = self.slices[required_start_index]
            end_index = self.slices[required_start_index + demand_slices + 1]
            if start_index == 0 and end_index == 0:
                return True, required_start_index

        empty_in_row = 0
        start_index = 0
        for index, is_empty in enumerate(self.slices):
            if is_empty == 0:
                empty_in_row = empty_in_row + 1
                if empty_in_row == demand_slices + 1 and start_index not in already_checked:
                    return True, start_index
            else:
                empty_in_row = 0
                start_index = index

        return False, required_start_index

    # Physical adding of removing space on core

    def allocate_for_demand(self, demand_id, demand_slices, start_index):
        self.indexes[demand_id] = start_index
        for index, chunk in enumerate((demand_slices + 1) * [1]):
            self.slices[self.indexes[demand_id] + index] = chunk

    def unallocate_for_demand(self, demand_id, demand_slices):
        start_index = self.indexes[demand_id]
        self.indexes.pop(demand_id)
        for index, chunk in enumerate((demand_slices + 1) * [0]):
            self.slices[start_index + index] = chunk

    def get_slices_numbers(self):
        empty_slices = len(list(filter(lambda slice: slice == 0, self.slices)))
        taken_slices = len(self.slices) - empty_slices

        return empty_slices, taken_slices