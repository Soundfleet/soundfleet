"""
storages.py AUDIO_TRACKS_STORAGE example for AWS s3
"""
from environ import Env


_env = Env(
    AWS_S3_ACCESS_KEY_ID=(str, "dummy"),
    AWS_S3_SECRET_ACCESS_KEY=(str, "dummy"),
    AWS_S3_SIGNATURE_VERSION=(str, "s3v4"),
    AWS_S3_REGION_NAME=(
        str,
        "eu-central-1",
    ),  # refer to aws docs for available regions
    AWS_STORAGE_BUCKET_NAME=(str, "dummy"),
    AWS_QUERYSTRING_EXPIRE=(
        int,
        60 * 60 * 24,
    ),  # expiration of generated url to file
)


AUDIO_TRACKS_STORAGE = {
    "storage_class": "media.storage.s3.Storage",
    "storage_conf": {
        "AWS_S3_ACCESS_KEY_ID": _env("AWS_S3_ACCESS_KEY_ID"),
        "AWS_S3_SECRET_ACCESS_KEY": _env("AWS_S3_SECRET_ACCESS_KEY"),
        "AWS_S3_SIGNATURE_VERSION": _env("AWS_S3_SIGNATURE_VERSION"),
        "AWS_S3_REGION_NAME": _env("AWS_S3_REGION_NAME"),
        "AWS_STORAGE_BUCKET_NAME": _env("AWS_STORAGE_BUCKET_NAME"),
        "AWS_QUERYSTRING_EXPIRE": _env("AWS_QUERYSTRING_EXPIRE"),
    },
}
