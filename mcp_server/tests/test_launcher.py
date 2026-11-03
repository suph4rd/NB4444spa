import contextlib
import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import launch
from nb4444_mcp.launcher.application import Launcher
from nb4444_mcp.launcher.configuration import (
    Environment, EnvironmentResolver, PROCESS_ENVIRONMENT_KEYS,
)
from nb4444_mcp.launcher.docker import DockerComposeRunner
from nb4444_mcp.launcher.locking import ComposeStartupLock


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / 'mcp_server' / 'env').mkdir(parents=True)
        self.resolver = EnvironmentResolver(self.root)

    def configure(self, mode, value='valid'):
        path = self.root / 'mcp_server' / 'env' / ('.env.prod' if mode == 'prod' else '.env')
        path.write_text('\n'.join(f'{key}="{value}"' for key in PROCESS_ENVIRONMENT_KEYS[:3]))
        return path

    def test_explicit_and_automatic_environment(self):
        for mode in Environment:
            with self.subTest(mode=mode):
                path = self.configure(mode.value)
                config = self.resolver.resolve(mode)
                self.assertEqual(config.environment, mode)
                self.assertEqual(config.env_file, path)
                self.assertEqual(self.resolver.resolve(), config)
                self.assertEqual(config.compose_file.name, 'docker-compose-prod.yml'
                                 if mode == Environment.PROD else 'docker-compose.yml')
                path.unlink()
        self.configure('dev')
        self.configure('prod')
        for mode in Environment:
            self.assertEqual(self.resolver.resolve(mode).environment, mode)

    def test_ambiguous_or_missing_environment(self):
        with self.assertRaisesRegex(ValueError, 'оба окружения либо ни одного'):
            self.resolver.resolve()
        self.configure('dev')
        self.configure('prod')
        with self.assertRaisesRegex(ValueError, 'оба окружения либо ни одного'):
            self.resolver.resolve()

    def test_placeholders_and_missing_values(self):
        for value in ('', 'REPLACE', 'your_token', 'token_value', 'changeme'):
            self.configure('dev', value)
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'dev: настройте'):
                self.resolver.resolve(Environment.DEV)
        path = self.configure('dev')
        path.write_text('NB4444_API_URL=valid')
        with self.assertRaises(ValueError):
            self.resolver.resolve(Environment.DEV)

    def test_docker_commands_environment_lock_and_stderr(self):
        self.configure('dev')
        config = self.resolver.resolve()
        events = []
        @contextlib.contextmanager
        def lock(compose):
            self.assertEqual(compose, config.compose_file)
            events.append('lock')
            yield
            events.append('unlock')
        def up(*args, **kwargs):
            events.append('up')
            return 0
        def execute(*args, **kwargs):
            events.append('exec')
        stderr = io.StringIO()
        env = dict.fromkeys(PROCESS_ENVIRONMENT_KEYS, 'remove') | {'PATH': '/bin', 'OTHER': 'keep'}
        with patch.dict('os.environ', env, clear=True), contextlib.redirect_stderr(stderr), \
                patch('nb4444_mcp.launcher.application.ComposeStartupLock', lock), \
                patch('nb4444_mcp.launcher.docker.subprocess.call', side_effect=up) as call, \
                patch('nb4444_mcp.launcher.docker.os.execvpe', side_effect=execute) as execvpe:
            Launcher(self.resolver, DockerComposeRunner()).run()
        clean = {'PATH': '/bin', 'OTHER': 'keep'}
        command = ['docker', 'compose', '-f', str(config.compose_file), '--env-file', str(config.env_file)]
        call.assert_called_once_with(command + ['up', '-d', '--no-deps', 'mcp'], env=clean, stdout=stderr)
        execvpe.assert_called_once_with('docker', command + ['exec', '-T', 'mcp', 'python', '/app/server.py'], clean)
        self.assertEqual(events, ['lock', 'up', 'unlock', 'exec'])
        self.assertEqual(stderr.getvalue(), 'NB4444 MCP: dev\n')

    def test_failed_up_returns_code_without_exec(self):
        self.configure('prod')
        with patch('nb4444_mcp.launcher.application.ComposeStartupLock') as lock, \
                patch('nb4444_mcp.launcher.docker.subprocess.call', return_value=17), \
                patch('nb4444_mcp.launcher.docker.os.execvpe') as execute, \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(Launcher(self.resolver, DockerComposeRunner()).run(), 17)
            execute.assert_not_called()
            lock.return_value.__exit__.assert_called_once()

    def test_lock_path_acquisition_and_release(self):
        compose = self.root / 'docker' / 'docker-compose.yml'
        lock = ComposeStartupLock(compose)
        self.assertEqual(lock.path.name, 'nb4444-mcp-' + hashlib.sha256(str(compose).encode()).hexdigest() + '.lock')
        file = Mock()
        with patch.object(Path, 'open', return_value=file) as opened, \
                patch('nb4444_mcp.launcher.locking.fcntl.flock') as flock:
            with self.assertRaisesRegex(RuntimeError, 'failure'):
                with lock:
                    flock.assert_called_once()
                    self.assertEqual(flock.call_args.args[0], file)
                    raise RuntimeError('failure')
        opened.assert_called_once_with('a')
        file.close.assert_called_once()

    def test_cli_errors_and_exit_code(self):
        with patch.object(launch.Launcher, 'run', side_effect=ValueError('ошибка конфигурации')), \
                contextlib.redirect_stderr(io.StringIO()) as stderr:
            with self.assertRaises(SystemExit) as error:
                launch.main([])
        self.assertEqual(error.exception.code, 2)
        self.assertIn('ошибка конфигурации', stderr.getvalue())
        with patch.object(launch.Launcher, 'run', return_value=23) as run:
            self.assertEqual(launch.main(['--env', 'prod']), 23)
            run.assert_called_once_with(Environment.PROD)


if __name__ == '__main__':
    unittest.main()
