from enum import Enum

from pydantic import BaseModel


class StorageType(Enum):
    S3 = "s3"
    ABS = "abs"
    ADLS = "adls"
    GCS = "gcs"


class Credential(BaseModel):
    url: str
    headers: dict[str, str]


class CreatePayload(BaseModel):
    path: str
    num_parts: int


class CreateResponse(BaseModel):
    type: StorageType
    creds: list[Credential]
    upload_id: str | None


class CompletePayload(BaseModel):
    path: str
    upload_id: str
    part_ids: list[str]


class CompleteResponse(BaseModel):
    pass


class AbortPayload(BaseModel):
    path: str
    upload_id: str


class AbortResponse(BaseModel):
    pass


class UploadUrlPayload(BaseModel):
    path: str
    upload_id: str
    part_id: str


class UploadUrlResponse(BaseModel):
    cred: Credential
