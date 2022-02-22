import hashlib
import magic

from typing import IO


class HashedStorageMixin:

    _rippers = {
        "audio/mpeg": "media.storage.rippers.mp3",
        # TODO: add more rippers (for ogg, wav, etc..)
    }
    _default_ripper = "media.storage.rippers.dummy"

    def get_hashed_name(self, content: IO[bytes]) -> str:
        content.seek(0)
        mime_type = self._detect_mime_type(content)
        ripper_module = __import__(
            self._mime_type_to_ripper(mime_type), {}, {}, ["essence"]
        )
        essence, size, extension = ripper_module.essence(content)

        name = hashlib.sha1(mime_type.encode("utf-8"))
        if hasattr(essence, "read"):
            total = 0
            while True:
                if size and total + 4096 > size:
                    buf = essence.read(total + 4096 - size)
                    name.update(buf)
                    break
                else:
                    buf = essence.read(4096)
                    total += 4096
                if not buf:
                    break
                name.update(buf)
        elif isinstance(essence, str):
            name.update(essence.encode("utf-8"))
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

    def _mime_type_to_ripper(self, mime_type):
        return self._rippers.get(mime_type, self._default_ripper)
