## Nodes
import datetime
import getopt
import sys
import time

from Demand import Demand
import os

## Consts
from FileParser.FileParser import FileParser
from Logger.Logger import Logger
from Topology import Topology

TOTAL_DURATION = 2000
PROCEED = True


def get_time(duration):
    return str(datetime.timedelta(seconds=int(duration)))


def run(all_demands: [Demand], topology: Topology) -> float:
    Logger.create_summary_file()
    demands = all_demands[:5]
    print("Total demands: {}".format(len(demands)))
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
        Logger.progress_bar(iteration, TOTAL_DURATION, get_time(current_duration))
        iteration = iteration + 1

    duration = time.time() - start
    print("\n Finished. Total time duration: {}".format(get_time(duration)))
    return duration


def main(argv):
    prog_spec = 'main.py -e <entry_dir> -d <demands_file> -c <number_of_cores> [-s] \n'
    entry_dir = ''
    demands_file = ''
    number_of_cores = ''
    write_summary_file = False

    try:
        opts, args = getopt.getopt(argv, "he:d:c:s", ["entry=", "dfile=", "cores=", "summary"])

        if len(opts) == 0:
            raise getopt.GetoptError(prog_spec)

        if '-h' in opts[0]:
            print(prog_spec)
            print('-e, --entry <entry_dir> \t Absolute path to directory with files (must end with /)')
            print('-d, --dfile <demands_file> \t Full name of file with demands')
            print('-c, --cores <number_of_cores> \t Number of cores in a single link (must be > 0)')
            print('-s, --summary \t \t \t Generates a brief summary in a format: <demands_file>_summary.csv')
            sys.exit()

        if len(opts) < 3:
            raise getopt.GetoptError(prog_spec)

        entry = opts[0][1]
        dfile = opts[1][1]
        cores = opts[2][1]

        if not os.path.isdir(entry):
            raise getopt.GetoptError('Directory not found: {}'.format(entry))
        if not os.path.isfile(entry + dfile):
            raise getopt.GetoptError('File not found: {}'.format(entry + dfile))
        if len(cores) < 1:
            raise getopt.GetoptError('There has to be at least one core. Given {}'.format(cores))

    except getopt.GetoptError as err:
        print(err)
        print("Try -h, --help for help")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-e", "--entry"):
            entry_dir = arg
        elif opt in ("-d", "--dfile"):
            demands_file = arg
        elif opt in ("-c", "--cores"):
            number_of_cores = arg
        elif opt in ("-s", "--summary"):
            write_summary_file = True

    file_parser = FileParser(entry_dir, demands_file, number_of_cores)
    demands, topology, dem_spec = file_parser.run()

    print("Entry directory: {}".format(entry_dir))
    print("Demands file: {}".format(demands_file))
    print("Number of cores: {}".format(number_of_cores))
    duration = run(demands, topology)

    if write_summary_file:
        Logger.create_final_summary(dem_spec, demands_file, number_of_cores, duration)


if __name__ == "__main__":
    main(sys.argv[1:])
