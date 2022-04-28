import csv
from django.core.mail import send_mail

                                   
# Function for sending mail
def sending_mail(message,subject, email):
    send_mail(
        subject=subject,
        message=message,
        from_email= 'rennintech.com',
        recipient_list=[email],
        fail_silently=False,
    )


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


# Avoiding Circular imports

# Function to handle reading the content of the uploaded file and creating the diagnosis code records
def process_file(uploaded_file):
    try:
        reader = csv.DictReader(decode_utf8(uploaded_file))
        contents = [row for row in reader]
        return contents
    except Exception:
        []
