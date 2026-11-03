from dataclasses import dataclass
from enum import Enum
from pathlib import Path


PROCESS_ENVIRONMENT_KEYS = (
    'NB4444_API_URL', 'NB4444_ACCESS_TOKEN', 'NB4444_REFRESH_TOKEN',
    'NB4444_HTTP_TIMEOUT', 'NB4444_UPLOAD_DIR',
)


class Environment(str, Enum):
    DEV = 'dev'
    PROD = 'prod'


@dataclass(frozen=True)
class LaunchConfiguration:
    root: Path
    environment: Environment
    env_file: Path
    compose_file: Path


class EnvironmentResolver:

    def __init__(self, root: Path):
        self.root = root.resolve()

    @staticmethod
    def configured(path: Path) -> bool:
        if not path.is_file():
            return False
        values = {}
        for line in path.read_text().splitlines():
            key, sep, value = line.strip().partition('=')
            if sep:
                values[key] = value.strip().strip('\"\'')
        return all(values.get(key) and not any(marker in values[key].lower()
                   for marker in ('replace', 'your_', '_value', 'changeme'))
                   for key in PROCESS_ENVIRONMENT_KEYS[:3])

    def resolve(self, environment: Environment | None = None) -> LaunchConfiguration:
        paths = {
            Environment.DEV: self.root / 'mcp_server' / 'env' / '.env',
            Environment.PROD: self.root / 'mcp_server' / 'env' / '.env.prod',
        }
        if environment is None:
            available = [mode for mode, path in paths.items() if self.configured(path)]
            if len(available) != 1:
                raise ValueError('Укажите --env dev или --env prod: настроены оба окружения либо ни одного')
            environment = available[0]
        if not self.configured(paths[environment]):
            raise ValueError(f'{environment.value}: настройте API URL и JWT в {paths[environment]}')
        compose = 'docker-compose-prod.yml' if environment == Environment.PROD else 'docker-compose.yml'
        return LaunchConfiguration(self.root, environment, paths[environment], self.root / 'docker' / compose)
