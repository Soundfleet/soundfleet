from storages.backends.s3boto3 import S3Boto3Storage

from media.storage.mixins import HashedStorageMixin


class Storage(HashedStorageMixin, S3Boto3Storage):
    def save(self, name, content, max_length=None):
        name = self.get_hashed_name(content)
        return super().save(name, content, max_length=max_length)
