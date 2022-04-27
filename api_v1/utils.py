import csv
from django.shortcuts import get_object_or_404

# Local import
from api_v1.models import Category, DiagnosisCode

                                   
# Function for sending mail
def send_mail():
    pass


# Function for checking if an uploaded file is a csv file
def check_is_CSV(file_type):
    if file_type == 'text/csv':
        return True
    else:
        return False

#  Function to decode the contents of the uploaded file
def decode_utf8(input_iterator):
    for l in input_iterator:
        yield l.decode('utf-8')


# Function to handle reading the content of the uploaded file and creating the diagnosis code records
def create_diagnosis_code_from_csv(uploaded_file):
    try:
        reader = csv.DictReader(decode_utf8(uploaded_file))
        diagnosis_code_list = []
        for row in reader:
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
        return True
    except Exception:
        return False
