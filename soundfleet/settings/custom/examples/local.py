"""
storages.py AUDIO_TRACKS_STORAGE example for local file system
"""

AUDIO_TRACKS_STORAGE = {
    "storage_class": "media.storage.local.Storage",
    "storage_conf": {"prefix": "audio_tracks", "directory_structure": (2, 2)},
}
