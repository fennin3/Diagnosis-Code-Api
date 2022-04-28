from celery import shared_task
from django.shortcuts import get_object_or_404
from .utils import sending_mail

# local imports
from api_v1.models import Category, DiagnosisCode

@shared_task
def create_diagnosis_codes_async_task(contents, email):
    try:
        diagnosis_code_list = []
        for row in contents:
            category = get_object_or_404(Category, id=row['category'])
            diagnosis_code_list.append(
                DiagnosisCode(
                code=row['code'],
                full_code=row['full_code'],
                abbreviated_description=row['abbreviated_description'],
                full_description=row['full_description'],
                category=category)
                )
        DiagnosisCode.objects.bulk_create(diagnosis_code_list)
        
        sending_mail(message="Your diagnosis code records has been created successfully", subject="Diagnosis Codes File Upload", email=email)
        return True
    except Exception:
        return False
