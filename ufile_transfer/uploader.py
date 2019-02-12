import os
import magic
from google.cloud import storage


class Uploader:

    """Uploader is a google cloud storage client to update files
    to bucket.
    """

    def __init__(self, root_path, credential_path, gcs_path=None, download_list=None, bucket_name=None):
        # set credentials to environ GOOGLE_APPLICATION_CREDENTIALS
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path
        self._root_path = root_path
        self._gcs_path = gcs_path or "legacy"
        self._client = storage.Client("vj-live-backend")
        self._bucket_name = bucket_name or "staging-user-uploaded"

    def upload(self, file_name:str, upload_fname:str=None):
        # if you want to overwrite the file name to be saved
        # you can give the upload_fname or it will use the default
        # rule to generateh the name
        bucket = self._client.bucket(self._bucket_name)
        # permission... fuck, we can not access bucket itself..
        # but we can access the content inside bucket what the f?
        # so there is no way to check whether this bucket exists or not.
        upload_file_name = upload_fname or file_name.split("/")[-1]

        # NOTE: maybe we can consider using https://github.com/ahupp/python-magic
        # to auto-detect content-type if we want to make this lib more general
        with open(file_name, 'rb') as f:
            name = os.path.join(self._gcs_path, upload_file_name)
            blob = bucket.blob(name)

            content_type = magic.from_file(file_name, mime=True)
            # use magic to determine the content_type
            # why I use this? because there are lots of fucking unknown file
            # without extension name
            # see: screenshot: https://imgur.com/aHg7754
            blob.upload_from_file(f, content_type=content_type) # file will be overwritten if exist
            blob.make_public()

        print(blob.public_url)

    def batch_upload(self, files):
        # NOTE: currently, google doesn't supprot batch upload..
        # see https://cloud.google.com/storage/docs/json_api/v1/how-tos/batch
        # so with self._client.batch() will not work..
        # use multi process?
        pass
