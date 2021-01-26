import os

from . import (
    aws_access_key_id,
    aws_s3_bucket,
    aws_s3_endpoint,
    aws_secret_access_key,
    base_path,
    pp,
)
from .ingest import Ingestor
from .s3 import S3


class Archive:
    def __init__(self):
        """
        Initialize the Archive class instance
        """
        self.ingestor = Ingestor()
        self.s3 = S3(
            aws_access_key_id, aws_secret_access_key, aws_s3_endpoint, aws_s3_bucket
        )

    def __call__(
        self,
        path: str,
        output_format: str,
        push: bool = False,
        clean: bool = False,
        latest: bool = False,
        *args,
        **kwargs
    ):
        """
        The `__call__` method allows a user to call a class instance with parameters.

        Parameters
        ----------
        path: path to the configutation file
        output_format: currently supported formats: `'csv'`, `'geojson'`, `'shapefile'`, `'postgres'`
        push: if `True` then push to s3
        clean: if `True`, the temporary files created under `.library` will be removed
        latest: if `True` then tag this current version we are processing to be the `latest`

        Sample Usage
        ----------
        ### A flat file example:
        ```python
        from library.archive import Archive
        a = Archive()
        a(
            "path/to/config.yml",
            output_format="csv", push=True, clean=True,
            latest=True, compress=True,
        )
        ```
        ### A postgres example:
        > by default, for postgres `push`, `clean`, `latest`, `compress` are all default to `False`
        ```python
        postgres_url='postgresql://user:password@hose/db'
        a(
            "path/to/config.yml",
            output_format="postgres",
            postgres_url=postgres_url,
        )
        ```
        """
        # Get ingestor by format
        ingestor_of_format = getattr(self.ingestor, output_format)

        # Initiate ingestion
        output_files, version, acl = ingestor_of_format(path, *args, **kwargs)
        print(output_files)

        # Write to s3
        for _file in output_files:
            if push:
                key = _file.replace(base_path + "/", "")
                self.s3.put(_file, key, acl)
            if push and latest:
                self.s3.put(_file, key.replace(version, "latest"), acl)
            if clean:
                os.remove(_file)
