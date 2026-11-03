#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys

from nb4444_mcp.launcher.application import Launcher
from nb4444_mcp.launcher.configuration import Environment, EnvironmentResolver
from nb4444_mcp.launcher.docker import DockerComposeRunner


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env', choices=('dev', 'prod'))
    args = parser.parse_args(argv)
    launcher = Launcher(
        EnvironmentResolver(Path(__file__).resolve().parent.parent),
        DockerComposeRunner(),
    )
    try:
        return launcher.run(Environment(args.env) if args.env else None)
    except ValueError as error:
        parser.error(str(error))


if __name__ == '__main__':
    sys.exit(main())
