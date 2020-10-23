from argparse import ArgumentParser

from utils import run_script


def main():
    parser = ArgumentParser(description='Run a migration script.')
    parser.add_argument('script', help='Script to run')
    parser.add_argument('config', help='Service config file')
    parser.add_argument('secrets', help='Service database admin secrets')

    args = parser.parse_args()
    run_script(args.script, args.config, args.secrets)


if __name__ == '__main__':
    main()
