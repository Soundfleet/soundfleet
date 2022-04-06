import hashlib
import magic

from typing import IO


class HashedStorageMixin:

    _extensions = {
        "audio/mpeg": "mp3",
        "audio/ogg": "ogg",
    }

    def get_hashed_name(self, content: IO[bytes]) -> str:
        content.seek(0)
        mime_type = self._detect_mime_type(content)

        size = self._get_size(content)
        extension = self._extensions.get(mime_type, "")

        name = hashlib.sha1(mime_type.encode("utf-8"))
        if hasattr(content, "read"):
            total = 0
            while True:
                if size and total + 4096 > size:
                    buf = content.read(total + 4096 - size)
                    name.update(buf)
                    break
                else:
                    buf = content.read(4096)
                    total += 4096
                if not buf:
                    break
                name.update(buf)
        elif isinstance(content, str):
            name.update(content.encode("utf-8"))
        content.seek(0)
        return (
            "{}.{}".format(name.hexdigest(), extension)
            if extension
            else name.hexdigest()
        )

    def _detect_mime_type(self, content):
        mime_type = magic.from_buffer(content.read(), mime=True)
        content.seek(0)
        return mime_type

    def _get_size(self, content):
        content.seek(0)
        size = len(content.read())
        content.seek(0)
        return size
