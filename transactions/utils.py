import uuid
from transactions.models import Transaction

def generate_unique_reference():
    while True:
        reference = f"REF-{uuid.uuid4().hex[:10].upper()}"
        if not Transaction.objects.filter(reference_number=reference).exists():
            return reference
