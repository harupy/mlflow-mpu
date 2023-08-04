import os

import boto3
from fastapi import FastAPI

import models as m

app = FastAPI()

BUCKET = os.environ["S3_BUCKET"]


@app.post("/mpu/create")
async def create(payload: m.CreatePayload) -> m.CreateResponse:
    s3 = boto3.client("s3")
    response = s3.create_multipart_upload(
        Bucket=BUCKET,
        Key=payload.path,
    )
    upload_id = response["UploadId"]
    creds = []
    for i in range(payload.num_parts):
        response = s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": BUCKET,
                "Key": payload.path,
                "PartNumber": i,
                "UploadId": upload_id,
            },
        )
        creds.append(
            m.Credential(
                url=response,
                headers={},
            )
        )

    return m.CreateResponse(type=m.StorageType.S3, creds=creds, upload_id=upload_id)


@app.post("/mpu/complete")
async def complete(payload: m.CompletePayload) -> m.CompleteResponse:
    s3 = boto3.client("s3")
    s3.complete_multipart_upload(
        Bucket=BUCKET,
        Key=payload.path,
        UploadId=payload.upload_id,
        MultipartUpload={
            "Parts": [
                {"PartNumber": i, "ETag": part_id} for i, part_id in enumerate(payload.part_ids)
            ]
        },
    )
    return m.CompleteResponse()


@app.post("/mpu/abort")
async def abort(payload: m.AbortPayload) -> m.AbortResponse:
    s3 = boto3.client("s3")
    s3.abort_multipart_upload(
        Bucket=BUCKET,
        Key=payload.path,
        UploadId=payload.upload_id,
    )
    return m.AbortResponse()


@app.post("/mpu/upload-url")
async def upload_url(payload: m.UploadUrlPayload) -> m.UploadUrlResponse:
    s3 = boto3.client("s3")
    response = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": BUCKET,
            "Key": payload.path,
            "PartNumber": payload.part_id,
            "UploadId": payload.upload_id,
        },
    )
    return m.UploadUrlResponse(cred=m.Credential(url=response, headers={}))
