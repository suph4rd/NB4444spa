import os
import subprocess
import sys

from .configuration import PROCESS_ENVIRONMENT_KEYS


class DockerComposeRunner:

    @staticmethod
    def process_environment(environ):
        return {key: value for key, value in environ.items() if key not in PROCESS_ENVIRONMENT_KEYS}

    @staticmethod
    def command(configuration):
        return ['docker', 'compose', '-f', str(configuration.compose_file),
                '--env-file', str(configuration.env_file)]

    def prepare_container(self, configuration, environ):
        return subprocess.call(
            self.command(configuration) + ['up', '-d', '--no-deps', 'mcp'],
            env=environ, stdout=sys.stderr)

    def exec_stdio(self, configuration, environ):
        os.execvpe('docker', self.command(configuration) + [
            'exec', '-T', 'mcp', 'python', '/app/server.py'], environ)
