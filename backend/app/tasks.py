from celery import shared_task

@shared_task
def process_document(doc_id: str) -> bool:
    # Placeholder for OCR/indexing pipeline
    print(f"Processing document {doc_id}")
    return True
