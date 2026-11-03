import fcntl
import hashlib
import tempfile
from pathlib import Path


class ComposeStartupLock:

    def __init__(self, compose_file: Path):
        lock_id = hashlib.sha256(str(compose_file).encode()).hexdigest()
        self.path = Path(tempfile.gettempdir()) / f'nb4444-mcp-{lock_id}.lock'
        self.file = None

    def __enter__(self):
        self.file = self.path.open('a')
        try:
            fcntl.flock(self.file, fcntl.LOCK_EX)
        except BaseException:
            self.file.close()
            raise
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
