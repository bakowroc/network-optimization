import getopt
import re
import sys

from numpy import genfromtxt

from Logger.Logger import Logger


def main(argv):
    bigcsv = ''
    smallcsv = ''

    try:
        opts, args = getopt.getopt(argv, "b:v", ["bigcsv=", "smallcsv="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-b", "--bigcsv"):
            bigcsv = arg
        elif opt in ("-v", "--smallcsv"):
            smallcsv = arg

    fix_csv(bigcsv, smallcsv)


def fix_csv(bigcsv, smallcsv):
    summary_data = genfromtxt(smallcsv, delimiter=';', dtype='U')
    filename = re.search('/([0-9]+_[0-9]+)', smallcsv).group(1)
    demands_file = "{}.dem".format(filename)
    dem_spec = {
        'net_avg': summary_data[1][0]
    }
    number_of_cores = summary_data[1][4]
    duration = summary_data[1][5]

    Logger.create_final_summary(dem_spec, demands_file, number_of_cores, duration, 'summary_fixed', bigcsv)


if __name__ == "__main__":
    main(sys.argv[1:])