import csv
import re
import argparse
import importlib
import sys

from csvgroup.common import dump_as_csv


def to_target_expression_pair(rule):
    match = re.match(
        r"(?P<target>[^=]+?)\s*=\s*(?P<expression>.+)",
        rule
    )

    if match is None:
        raise ValueError("Invalid rule: {}".format(rule))

    return (match.group("target"), match.group("expression"))


def apply_rules(rules, item, imported_module):
    mapped = item.copy()
    environment = item.copy()

    if imported_module:
        environment[imported_module.__name__] = imported_module

    for target, expression in rules:
        try:
            mapped[target] = eval(expression, environment)
        except ValueError:
            mapped[target] = None

    return mapped


def process(items, rules, imported_module):
    def new_fieldnames():
        return [target
                for target, expression in rules
                if target not in items.fieldnames]

    fieldnames = items.fieldnames + new_fieldnames()

    yield fieldnames

    for item in items:
        mapped = apply_rules(rules, item, imported_module)

        yield [mapped.get(field) for field in fieldnames]


def arguments():
    parser = argparse.ArgumentParser(
        description="By-row mapping of fields in CSV files"
    )
    parser.add_argument(
        "--import-module",
        "-i",
        help="module to import for the operation"
    )
    parser.add_argument(
        "rules",
        metavar="rule",
        nargs="+",
        help=(
            "rule to perform on fields "
            + "(e.g., 'left_majority = int(left) > int(right)')"
        )
    )

    return parser.parse_args()


def main():
    args = arguments()

    rules = [to_target_expression_pair(rule) for rule in args.rules]
    imported_module = None

    if args.import_module:
        imported_module = importlib.import_module(args.import_module)

    dump_as_csv(
        process(
            csv.DictReader(sys.stdin),
            rules,
            imported_module
        )
    )


if __name__ == "__main__":
    main()
