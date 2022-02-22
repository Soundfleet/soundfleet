from django.core.files.storage import FileSystemStorage

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
