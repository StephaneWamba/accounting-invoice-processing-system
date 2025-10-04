from pydantic import BaseModel, Field
from typing import Optional


class IngestRequest(BaseModel):
    objectKey: str = Field(..., description="S3 object key for original file")
    accountId: Optional[str] = Field(default=None)
    vendorId: Optional[int] = Field(default=None)


class IngestResponse(BaseModel):
    invoiceId: int
    status: str
