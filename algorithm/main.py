## Nodes
import datetime
import getopt
import shutil
import sys
import time

from Demand import Demand
from Link.Link import Link
import os
import numpy as np
import matplotlib.pyplot as plt

## Consts
from FileParser.FileParser import FileParser
from Topology import Topology

TOTAL_DURATION = 2000
PROCEED = True


def show_chart(link: Link):
    legend = []
    for core in link.cores:
        filename = './data/{}/{}_{}_results.csv'.format(link.id, link.id, core.id)
        data = np.genfromtxt(filename, delimiter=',', names=['iteration', 'slices'])
        legend.append("Core {}".format(core.id))
        plt.plot(data['iteration'], data['slices'],  linewidth=2)

    plt.legend(legend)
    plt.title("Link {}".format(link.id))
    plt.xlabel('Iterations')
    plt.ylabel('Slices taken')
    plt.show(block=True)


def get_time(duration):
    return str(datetime.timedelta(seconds=int(duration)))


def progress_bar(value, endvalue, current_duration, bar_length=80):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rProgress: [{0}] {1}% {2}".format(arrow + spaces, int(round(percent * 100)), current_duration))
    sys.stdout.flush()


def create_summary_file():
    filename = "./demands_summary.csv"
    if os.path.isfile(filename):
        os.remove(filename)

    with open(filename, "a") as file:
        file.write('{}; {}; {}; {}; {}; {}; {}; {}; {}; {}; {}\n'.format(
            "Demand ID",
            "Started at",
            "Source Node",
            "Destination node",
            "Bitrate",
            "Duration",
            "Is success",
            "Links in path",
            "Path length",
            "Required core",
            "Required index"
        ))
        file.close()


def run(all_demands: [Demand], topology: Topology):
    create_summary_file()
    demands = all_demands
    iteration = 0
    start = time.time()

    while iteration <= TOTAL_DURATION and PROCEED:
        demands_starting_now = list(filter(lambda demand: demand.started_at == iteration, demands))
        demands_finishing_now = list(filter(lambda demand: demand.started_at + demand.duration == iteration, demands))
        prepared_demands = set(demands_starting_now + demands_finishing_now)

        for demand in prepared_demands:
            paths_candidates = topology.get_paths(demand.source.id, demand.destination.id)
            number_of_paths = len(paths_candidates)
            chosen_path = 0
            if number_of_paths > 0:
                while chosen_path < number_of_paths:
                    is_success = demand.check_and_allocate(iteration, paths_candidates[chosen_path])

                    if is_success:
                        break
                    else:
                        chosen_path = chosen_path + 1
            else:
                demand.mark_as_failed()

        current_duration = time.time() - start
        progress_bar(iteration, TOTAL_DURATION, get_time(current_duration))
        iteration = iteration + 1

    duration = time.time() - start
    print("\n Finished. Total time duration: {}s".format(get_time(duration)))


def main(argv):
    entry_dir = ''
    demands_file = ''

    try:
        opts, args = getopt.getopt(argv, "he:d:", ["entry=", "dfile="])

        if len(opts) < 2:
            print(opts)
            raise getopt.GetoptError('main.py -e <entry_dir> -d <demands_file>')

        entry = opts[0][1]
        dfile = opts[1][1]

        if not os.path.isdir(entry):
            raise getopt.GetoptError('Directory not found: {}'.format(entry))
        if not os.path.isfile(entry + dfile):
            raise getopt.GetoptError('File not found: {}'.format(entry + dfile))

    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('main.py -e <entry_dir> -d <demands_file>')
            sys.exit()
        elif opt in ("-e", "--entry_dir"):
            entry_dir = arg
        elif opt in ("-d", "--dfile"):
            demands_file = arg

    file_parser = FileParser(entry_dir, demands_file)
    demands, topology = file_parser.run()

    run(demands, topology)


if __name__ == "__main__":
    main(sys.argv[1:])
