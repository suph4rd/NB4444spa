import os
import sys

from .locking import ComposeStartupLock


class Launcher:

    def __init__(self, resolver, runner):
        self.resolver = resolver
        self.runner = runner

    def run(self, environment=None):
        configuration = self.resolver.resolve(environment)
        environ = self.runner.process_environment(os.environ)
        print(f'NB4444 MCP: {configuration.environment.value}', file=sys.stderr)
        with ComposeStartupLock(configuration.compose_file):
            result = self.runner.prepare_container(configuration, environ)
            if result:
                return result
        self.runner.exec_stdio(configuration, environ)
