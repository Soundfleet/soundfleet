import errno
import os

from django.conf import settings
from django.core.files import locks
from django.core.files.storage import FileSystemStorage
from django.core.files.move import file_move_safe
from django.utils._os import safe_join

from media.storage.mixins import HashedStorageMixin


class Storage(HashedStorageMixin, FileSystemStorage):
    def __init__(
        self,
        prefix: str = "",
        directory_structure: tuple[int, int] = (2, 2),
        *args,
        **kwargs,
    ) -> None:
        self.prefix = prefix
        self.directory_structure = directory_structure
        super().__init__(*args, **kwargs)

    def save(self, name, content, max_length=None):
        name = self.get_hashed_name(content)

        full_path = self.path(name)

        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        elif not os.path.isdir(directory):
            raise IOError(
                "{} exists and is not a directory.".format(directory)
            )

        try:
            # This file has a file path that we can move.
            if hasattr(content, "temporary_file_path"):
                file_move_safe(content.temporary_file_path(), full_path)
                content.close()
            # This is a normal uploaded file that we can stream.
            else:
                # This fun binary flag incantation makes os.open throw an
                # OSError if the file already exists before we open it.
                fd = os.open(
                    full_path,
                    os.O_WRONLY
                    | os.O_CREAT
                    | os.O_EXCL
                    | getattr(os, "O_BINARY", 0),
                )
                try:
                    locks.lock(fd, locks.LOCK_EX)
                    if hasattr(content, "chunks"):
                        for chunk in content.chunks():
                            os.write(fd, chunk)
                    else:
                        os.write(fd, content.read())
                finally:
                    locks.unlock(fd)
                    os.close(fd)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        if settings.FILE_UPLOAD_PERMISSIONS is not None:
            os.chmod(full_path, settings.FILE_UPLOAD_PERMISSIONS)

        return name

    def path(self, name):
        paths = self._relative_path(name)
        return safe_join(self.location, *paths)

    def url(self, name):
        name = os.path.join(*self._relative_path(name))
        return super().url(name)

    def _relative_path(self, name):
        paths = [getattr(self, "prefix", "")]
        index = 0
        for level in self.directory_structure:
            paths.append(name[index : index + level])
            index += level
        paths.append(name)
        return paths
