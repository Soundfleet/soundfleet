from typing import IO


def essence(content: IO[bytes]) -> tuple[IO[bytes], int, str]:
    content.seek(0)
    size = len(content.read())
    content.seek(0)
    return content, size, ""
