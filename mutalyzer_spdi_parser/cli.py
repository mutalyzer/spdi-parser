"""
CLI entry point.
"""

import argparse
import json

from lark.tree import pydot__tree_to_png

from . import usage, version
from .spdi_parser import parse
from .convert import parse_tree_to_model


def _parse(description, grammar_path):
    """
    CLI wrapper for parsing with no conversion to model.
    """
    parse_tree = parse(description, grammar_path)
    print("Successfully parsed:\n {}".format(description))
    return parse_tree


def _to_model(description, raw):
    """
    CLI wrapper for parsing, converting, and printing the model.
    """
    parse_tree = parse(description)
    model = parse_tree_to_model(parse_tree, raw)
    if isinstance(model, dict) or isinstance(model, list):
        print(json.dumps(model, indent=2))
    else:
        print(model)
    return parse_tree


def _arg_parser():
    """
    Command line argument parsing.
    """
    parser = argparse.ArgumentParser(
        description=usage[0],
        epilog=usage[1],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("description", help="the SPDI variant description to be parsed")

    parser.add_argument(
        "-c", action="store_true", help="convert the description to the model"
    )

    parser.add_argument(
        "-r", action="store_true", help="raw model"
    )

    parser.add_argument(
        "-i", help="save the parse tree as a PNG image (pydot required!)"
    )

    parser.add_argument("-v", action="version", version=version(parser.prog))

    return parser


def _cli(args):
    if args.c:
        parse_tree = _to_model(args.description, args.r)
    else:
        parse_tree = _parse(args.description)

    if args.i and parse_tree:
        pydot__tree_to_png(parse_tree, args.i)
        print("Parse tree image saved to:\n {}".format(args.i))


def main():

    parser = _arg_parser()

    args = parser.parse_args()

    _cli(args)


if __name__ == "__main__":
    main()
