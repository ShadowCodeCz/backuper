import argparse
import os

from . import cli
from . import app_core

def main():

    ac = app_core.AppCore()
    ac.set_standard_logger()

    parser = argparse.ArgumentParser(
        description=f"{ac.name}\n\n{ac.read_extended_help()}",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("-p", "--path", default=os.getcwd())
    parser.add_argument("--output_dir", default=os.path.join(ac.app_directory(), "%Y.%m.%d"))
    parser.add_argument("--remove", action='store_true')
    parser.set_defaults(func=cli.backup)

    arguments = parser.parse_args()
    arguments.func(arguments)

