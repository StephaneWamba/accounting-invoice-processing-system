import boto3
from botocore.client import Config
from typing import Tuple

from ..config import settings


def get_s3_client():
    return boto3.client(
        "s3",
        region_name=settings.aws_region,
        config=Config(s3={"addressing_style": "path"}),
    )


def generate_presigned_put_url(object_key: str, content_type: str, expires_in_seconds: int = 600) -> str:
    s3 = get_s3_client()
    return s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": settings.s3_bucket,
            "Key": object_key,
            "ContentType": content_type,
            "ServerSideEncryption": "AES256",
        },
        ExpiresIn=expires_in_seconds,
    )


def generate_presigned_get_url(object_key: str, expires_in_seconds: int = 600) -> str:
    s3 = get_s3_client()
    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": settings.s3_bucket,
            "Key": object_key,
        },
        ExpiresIn=expires_in_seconds,
    )
