from abc import ABC, abstractmethod
from datetime import timedelta

from aioboto3 import Session


class Storage(ABC):
    @abstractmethod
    async def generate_url(self, path: str) -> str:
        raise NotImplementedError


class S3Storage(Storage):
    def __init__(self, access_key: str, secret_key: str, endpoint: str, bucket_name: str, url_ttl: timedelta):
        self._session = Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

        self._bucket_name = bucket_name
        self._endpoint = endpoint
        self._url_ttl = int(url_ttl.total_seconds())
        self._service_name = "s3"

    async def generate_url(self, name: str) -> str:
        async with self._connection as client:
            return await client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self._bucket_name,
                    "Key": name,
                },
                ExpiresIn=self._url_ttl,
            )

    @property
    def _connection(self):
        return self._session.client(service_name=self._service_name, endpoint_url=self._endpoint)
