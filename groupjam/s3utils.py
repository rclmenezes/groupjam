# Modified from https://gist.github.com/3178905

from boto.utils import parse_ts
from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage

class ModifiedS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        super(ModifiedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(ModifiedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name
        
    def modified_time(self, name):
        name = self._normalize_name(self._clean_name(name))
        entry = self.entries.get(name)
        if entry is None:
            entry = self.bucket.get_key(self._encode_name(name))
        # Parse the last_modified string to a local datetime object.
        return parse_ts(entry.last_modified)

StaticRootS3BotoStorage = lambda: ModifiedS3BotoStorage(location='static')
MediaRootS3BotoStorage  = lambda: ModifiedS3BotoStorage(location='media')