import os
from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class ServerSettings:
    api_url: str = 'http://localhost:8008'
    access_token: str = field(default='', repr=False)
    refresh_token: str = field(default='', repr=False)
    http_timeout: float = 30
    upload_root: str | None = None

    @classmethod
    def from_environment(cls, environ: Mapping[str, str] | None = None) -> "ServerSettings":
        env = os.environ if environ is None else environ
        return cls(
            api_url=env.get('NB4444_API_URL', 'http://localhost:8008').rstrip('/'),
            access_token=env.get('NB4444_ACCESS_TOKEN', ''),
            refresh_token=env.get('NB4444_REFRESH_TOKEN', ''),
            http_timeout=float(env.get('NB4444_HTTP_TIMEOUT', '30')),
            upload_root=env.get('NB4444_UPLOAD_ROOT'),
        )
