from configparser import ConfigParser
from scholarly import scholarly
import questionary

PATH_CONFIG = "config.ini"


def get_author_id(args):
    if get_cfg('main.id') is None or args.reset:
        main(args)
    return get_cfg('main.id')


def cfg():
    config = ConfigParser()
    config.read(PATH_CONFIG)

    if not config.has_section('main'):
        config.add_section('main')
    return config


def get_cfg(fqkey):
    config = cfg()
    results = []
    section, key = fqkey.split('.', 1)
    if key in config.options(section):
        return config.get(section, key)


def set_cfg(fqkey_to_value):
    config = cfg()
    for fqkey, value in fqkey_to_value.items():
        section, key = fqkey.split('.', 1)
        config.set(section, key, value)
    with open(PATH_CONFIG, 'w') as f:
        config.write(f)


def add_parser(subparsers, parent):
    parser_config = subparsers.add_parser('config', parents=[parent])
    parser_config.add_argument('--key', default='main.id', help='config key')
    parser_config.add_argument('--set', help='save Google Scholar id')
    parser_config.add_argument('--get', action='store_true', help='get Google Scholar id')


def main(args):
    if args.get:
        print(get_cfg(args.key))
        return
    if args.set:
        set_cfg({args.key: args.set})
        print(f"Successfully saved author ID {args.set} to {PATH_CONFIG}")
        return
