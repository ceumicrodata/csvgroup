import csv
import sys


def dump_as_csv(items):
    (csv
     .writer(sys.stdout)
     .writerows(items))
