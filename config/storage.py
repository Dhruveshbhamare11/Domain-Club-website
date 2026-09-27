import os
from pathlib import Path
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class SafeFileSystemStorage(FileSystemStorage):
    """
    A resilient FileSystemStorage that intercepts read-only filesystem errors
    (common on serverless environments like Vercel / AWS Lambda where /var/task is read-only)
    and transparently redirects writes to /tmp/media to prevent 500 crashes.
    """

    def _save(self, name, content):
        try:
            return super()._save(name, content)
        except (OSError, PermissionError):
            tmp_dir = Path("/tmp/media")
            tmp_dir.mkdir(parents=True, exist_ok=True)
            orig_location = self.base_location
            self.base_location = str(tmp_dir)
            try:
                return super()._save(name, content)
            finally:
                self.base_location = orig_location
