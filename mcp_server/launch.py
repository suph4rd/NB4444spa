#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
KEYS = ('NB4444_API_URL', 'NB4444_ACCESS_TOKEN', 'NB4444_REFRESH_TOKEN',
        'NB4444_HTTP_TIMEOUT', 'NB4444_UPLOAD_DIR')


def configured(path):
    if not path.is_file():
        return False
    values = {}
    for line in path.read_text().splitlines():
        key, sep, value = line.strip().partition('=')
        if sep:
            values[key] = value.strip().strip('\"\'')
    return all(values.get(key) and not any(marker in values[key].lower()
               for marker in ('replace', 'your_', '_value', 'changeme'))
               for key in KEYS[:3])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env', choices=('dev', 'prod'))
    args = parser.parse_args()
    paths = {mode: ROOT / 'mcp_server' / filename for mode, filename in
             [('dev', '.env'), ('prod', '.env.prod')]}
    mode = args.env
    if mode is None:
        available = [name for name, path in paths.items() if configured(path)]
        if len(available) != 1:
            parser.error('Укажите --env dev или --env prod: настроены оба окружения либо ни одного')
        mode = available[0]
    if not configured(paths[mode]):
        parser.error(f'{mode}: настройте API URL и JWT в {paths[mode]}')
    compose = ROOT / 'docker' / ('docker-compose-prod.yml' if mode == 'prod' else 'docker-compose.yml')
    env = {key: value for key, value in os.environ.items() if key not in KEYS}
    print(f'NB4444 MCP: {mode}', file=sys.stderr)
    return subprocess.call(['docker', 'compose', '-f', str(compose), '--env-file',
                            str(paths[mode]), 'run', '--rm', '--no-deps', '-T', 'mcp'], env=env)


if __name__ == '__main__':
    sys.exit(main())
