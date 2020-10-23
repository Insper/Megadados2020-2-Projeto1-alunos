from argparse import ArgumentParser

from utils.utils import run_all_scripts


def main():
    parser = ArgumentParser(description='Run all migration scripts.')
    parser.add_argument('migrations_dir', help='Directory with the migrations')
    parser.add_argument('config', help='Service config file')
    parser.add_argument('secrets', help='Service database admin secrets')

    args = parser.parse_args()
    run_all_scripts(args.migrations_dir, args.config, args.secrets)


if __name__ == '__main__':
    main()
