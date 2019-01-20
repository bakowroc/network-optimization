import os
import sys

from numpy import genfromtxt

NO_PRINT = True
NO_WRITE = True


class Logger:
    @staticmethod
    def print(string):
        if not NO_PRINT:
            print(string)

    @staticmethod
    def write(write: lambda: int):
        if not NO_WRITE:
            write()

    @staticmethod
    def progress_bar(value, endvalue, current_duration, bar_length=20):
        percent = float(value) / endvalue
        arrow = '#' * int(round(percent * bar_length))
        spaces = '-' * (bar_length - len(arrow))

        sys.stdout.write(
            "\rProgress: [{0}] {1}% {2}".format(arrow + spaces, int(round(percent * 100)), current_duration))
        sys.stdout.flush()

    @staticmethod
    def create_summary_file():
        filename = "./demands_summary.csv"
        if os.path.isfile(filename):
            os.remove(filename)

        with open(filename, "a") as file:
            file.write('{}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}\n'.format(
                "Demand ID",
                "Started at",
                "Source Node",
                "Destination node",
                "Bitrate",
                "Duration",
                "Is success",
                "Links in path",
                "Path length",
                "Is shortest path",
                "Required core",
                "Required index"
            ))
            file.close()

    @staticmethod
    def create_final_summary(dem_spec, demands_file, number_of_cores, duration):
        demands_summary_file = './demands_summary.csv'
        summary_file_name = "./{}_summary.csv".format(demands_file)
        demands_data = genfromtxt(demands_summary_file, delimiter=';', dtype=None)

        if os.path.isfile(summary_file_name):
            os.remove(summary_file_name)

        number_of_shortest_paths = 0
        number_of_failures = 0
        total_demands = len(demands_data)

        for row in demands_data:
            if not bool(row[6]):
                number_of_failures = number_of_failures + 1

            if bool(row[9]):
                number_of_shortest_paths = number_of_shortest_paths + 1

        with open(summary_file_name, "a") as file:
            file.write('{}; {}; {}; {}; {}; {}\n {}; {}; {}; {}; {}; {}'.format(
                "Erlangs",
                "Total demands",
                "Failed",
                "Shortest",
                "Cores",
                "Duration",
                dem_spec['net_avg'],
                total_demands,
                number_of_failures,
                number_of_shortest_paths,
                number_of_cores,
                round(duration, 2)
            ))
            file.close()


