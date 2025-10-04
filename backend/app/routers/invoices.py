from fastapi import APIRouter, Depends, Query
from uuid import uuid4
from typing import Literal
from sqlalchemy.orm import Session

from ..auth import verify_api_key
from ..services.s3 import generate_presigned_put_url
from ..deps import get_db
from .. import models
from ..schemas import IngestRequest, IngestResponse
from backend.worker.tasks import extract_invoice

router = APIRouter(prefix="/invoices",
                   tags=["invoices"], dependencies=[Depends(verify_api_key)])


@router.get("/ping")
def ping() -> dict:
    return {"message": "pong"}


@router.post("/upload-url")
def create_upload_url(
    content_type: Literal["application/pdf", "image/png",
                          "image/jpeg"] = Query(..., alias="contentType"),
    account_id: str | None = Query(default=None),
) -> dict:
    object_key = f"{account_id or 'default'}/uploads/{uuid4()}"
    url = generate_presigned_put_url(
        object_key=object_key, content_type=content_type)
    return {"uploadUrl": url, "objectKey": object_key}


@router.post("/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest, db: Session = Depends(get_db)) -> IngestResponse:
    invoice = models.Invoice(
        account_id=None,
        vendor_id=req.vendorId,
        status="uploaded",
        confidence=None,
        totals_jsonb=None,
        extracted_jsonb=None,
        original_file_url=req.objectKey,
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    extract_invoice.delay(object_key=req.objectKey, invoice_id=invoice.id)

    return IngestResponse(invoiceId=invoice.id, status="processing")
