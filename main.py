"""Generates customizable publications webpage from a Google Scholar

1. Build bibtex from arxiv and google scholar
2. Generate webpage from bibtex
"""

from webfscholar import config, bibtex
import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    config.add_parser(subparsers)

    parser_build = subparsers.add_parser('bibtex')
    parser_web = subparsers.add_parser('web')
    return parser


def web(args):
    pass


command_to_function = {
    'config': config.main,
    'bibtex': bibtex.main,
    'web': web
}


def main():
    parser = get_parser()
    args = parser.parse_args()

    command = command_to_function.get(args.command, 'web')
    command(args)


if __name__ == '__main__':
    main()
