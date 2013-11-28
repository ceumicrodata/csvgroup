import csv
import itertools
import argparse
import importlib
import sys

from csvgroup.common import dump_as_csv


def cast_to_type(type, values):
    return [type(value) for value in values if value]


def aggregate(function, values, type):
    cast_values = cast_to_type(type, values)

    return function(cast_values) if cast_values else None


def get_values(column, items):
    return [item.get(column) for item in items]


def process(items, group, columns, function, type):
    def key(item):
        return [item.get(column) for column in group]

    def groups(items, key):
        return ((group_key, list(generator))
                for group_key, generator in itertools.groupby(
                                                sorted(items, key=key),
                                                key))

    fieldnames = group + columns

    yield fieldnames

    for group_key, group_items in groups(items, key):
        yield (group_key
               + [aggregate(
                    function,
                    get_values(column, group_items),
                    type)
                  for column in columns])


def arguments():
    parser = argparse.ArgumentParser(
                description="Perform group-by aggregation on CSV files")
    parser.add_argument(
        "--group",
        "-g",
        help="list of columns to group by, separated by comma")
    parser.add_argument(
        "--import-module",
        "-i",
        help="module to import for the operation")
    parser.add_argument(
        "--type",
        "-t",
        default="float",
        help="type of columns to aggregate (default: float)")
    parser.add_argument(
        "columns",
        help="list of columns to perform aggregation on, separated by comma")
    parser.add_argument(
        "function",
        help=("Python function that performs aggregation (e.g., 'sum' "
              + "or 'lambda v: 1. * sum(v) / len(v)')"))

    return parser.parse_args()


def main():
    args = arguments()

    environment = dict()

    if args.import_module:
        module = importlib.import_module(args.import_module)
        environment[module.__name__] = module

    group = args.group.split(",") if args.group else []
    columns = args.columns.split(",")
    function = eval(args.function, environment)
    type = eval(args.type, environment)

    dump_as_csv(
        process(
            csv.DictReader(sys.stdin),
            group,
            columns,
            function,
            type))


if __name__ == "__main__":
    main()
