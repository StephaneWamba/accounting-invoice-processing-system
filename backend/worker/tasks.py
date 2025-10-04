from .celery_app import celery_app


@celery_app.task(name="extract_invoice")
def extract_invoice(object_key: str, invoice_id: int) -> dict:
    # TODO: Download from S3 by object_key, call vision model, normalize, store in DB for invoice_id
    return {"status": "stub", "objectKey": object_key, "invoiceId": invoice_id}
