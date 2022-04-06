import struct

from typing import IO


def essence(content: IO[bytes]) -> tuple[IO[bytes], int, str]:
    content.seek(0)
    finish = len(content.read())
    # Detect ID3v1 tag if present
    content.seek(-128, 2)
    if content.read(3) == "TAG":
        finish -= 128
    # ID3 at the start marks ID3v2 tag (0-2)
    content.seek(0)
    start = content.tell()
    if content.read(3) == "ID3":
        # Bytes w major/minor version (3-4)
        content.read(2)  # version
        # Flags byte (5)
        flags = struct.unpack("B", content.read(1))[0]
        # Flat bit 4 means footer is present (10 bytes)
        footer = flags & (1 << 4)
        # Size of tag body synchsafe integer (6-9)
        bs = struct.unpack("BBBB", content.read(4))
        bodysize = (bs[0] << 21) + (bs[1] << 14) + (bs[2] << 7) + bs[3]
        # Seek to end of ID3v2 tag
        content.seek(bodysize, 1)
        if footer:
            content.seek(10, 1)
        start = content.tell()
    content.seek(start)
    return content, finish - start, "mp3"
