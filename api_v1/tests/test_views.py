from rest_framework.test import APITestCase,APIClient
from api_v1.models import DiagnosisCode, Category
from django.utils.http import urlencode
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import time


BASE_DIR = settings.BASE_DIR
base_url = 'diagnosis-list'
category_list = 'category-list'
category_detail = 'category-detail'

class TestViewListCreate(APITestCase):
    def setUp(self):
        # The APIClient() class helps us make request to our endpoints
        self.client = APIClient()

        #Setting up  variables of urls to make the code organized
        self.base_url = '/api/v1/codes/'

        #Creating one CategoryCode record to work with within the test
        self.category = Category.objects.create(title="Category Title",code="2190")

        #Creating one diagnosisCode record to work with within the test
        self.diagnosisCode = DiagnosisCode.objects.create(
            category=self.category,
            code="1123",
            abbreviated_description="Abbr Desc",
            full_description="full Description"
        )

    def test_diagnosisCode_list_GET(self):
        response = self.client.get(reverse(base_url))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']),1)


    def test_diagnosisCode_create_POST(self):
        req_body = {
            "category":self.category.id,
            "code":"2212",
            "abbreviated_description":"Abbr Desc 2",
            "full_description":"full Description 2"
        } 
        response = self.client.post(reverse('diagnosis-list'), req_body)
        self.assertEqual(response.status_code, 201)
        queryset_total = DiagnosisCode.objects.all().count()
        self.assertEqual(queryset_total,2)
    
    # Testing the create(POST) method with no data in the body of the request
    def test_diagnosisCode_create_no_data_POST(self):
        req_body = {} 
        response = self.client.post(self.base_url, req_body)
        self.assertEqual(response.status_code, 400)
        queryset_total = DiagnosisCode.objects.all().count()
        self.assertEqual(queryset_total,1)
    
    def test_diagnosisCode_create_invalid_data_POST(self):
        # 1. Testing code field max_length constraint
        req_body = {
            "category":self.category.id,
            "code":"2fdjfkfdhdhjfhdf",
            "abbreviated_description":"Abbr Desc 2",
            "full_description":"full Description 2"
        } 
        response = self.client.post(reverse('diagnosis-list'), req_body)
        self.assertEqual(response.status_code, 400)    

        # 2. Testing category field left blank
        req_body = {
            "category":"",
            "code":"123SC",
            "abbreviated_description":"Abbr Desc 2",
            "full_description":"full Description 2"
        } 
        response = self.client.post(self.base_url, req_body)
        self.assertEqual(response.status_code, 400) 


class TestRetrieveUpdateDelete(APITestCase):
    def setUp(self):
        self.client = APIClient()

        #Creating one Category record to work with within the test
        self.category = Category.objects.create(title="Category Title",code="2190")

        #Creating one diagnosisCode record to work with within the test
        self.diagnosisCode = DiagnosisCode.objects.create(
            category=self.category,
            code="1123",
            abbreviated_description="Abbr Desc",
            full_description="full Description"
        )
    # Testing the retrieve (GET) method and confirming that it return the correct data
    def test_diagnosisCode_retrieve_GET(self):
        response = self.client.get(f'{reverse(base_url)}{self.diagnosisCode.id}')

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['id'],self.diagnosisCode.id)
    
    # Testing the retrieve with wrong diagnosis code id
    def test_diagnosisCode_retrieve_Wrong_ID_GET(self):
        response = self.client.get(f'{reverse(base_url)}{20}')
        self.assertEqual(response.status_code,404)

    def test_diagnosisCode_update_PATCH(self):

        diagnosisCode = DiagnosisCode.objects.get(id=self.diagnosisCode.id)

        self.assertEqual(diagnosisCode.abbreviated_description, "Abbr Desc")
        self.assertEqual(diagnosisCode.code, "1123")

        req_body = {
            "abbreviated_description":"New Desc",
            "code":"2"
        }
        response = self.client.patch(f'{reverse(base_url)}{self.diagnosisCode.id}',req_body)

        # Checking status code of the request
        self.assertEqual(response.status_code, 200)
        # confirming that object was updated
        diagnosisCode = DiagnosisCode.objects.get(id=self.diagnosisCode.id)
        self.assertEqual(diagnosisCode.abbreviated_description, "New Desc")
        self.assertEqual(diagnosisCode.code, "2")

    def test_diagnosisCode_update_invalid_data_PATCH(self):

        diagnosisCode = DiagnosisCode.objects.get(id=self.diagnosisCode.id)

        self.assertEqual(diagnosisCode.abbreviated_description, "Abbr Desc")
        self.assertEqual(diagnosisCode.code, "1123")

        req_body = {
            "abbreviated_description":"New Desc",
            "code":"2Ttdtsdttvvghsvdgghsgdgs"  # max_character is 10
        }
        response = self.client.patch(f'{reverse(base_url)}{self.diagnosisCode.id}',req_body)

        # Checking status code of the request
        self.assertEqual(response.status_code, 400)

    # Testing the full update (PUT) method
    def test_diagnosisCode_update_PUT(self):
        diagnosisCode = DiagnosisCode.objects.get(id=self.diagnosisCode.id)
        self.assertEqual(diagnosisCode.abbreviated_description, "Abbr Desc")
        self.assertEqual(diagnosisCode.code, "1123")

        req_body = {
            "category":self.category.id,
            "code":"A55",
            "abbreviated_description":"Abbr Desc 2",
            "full_description":"full Description 2"
        }
        response = self.client.put(f'{reverse(base_url)}{self.diagnosisCode.id}',req_body)

        # Checking status code of the request
        self.assertEqual(response.status_code, 200)
        # confirming that object was updated
        diagnosisCode = DiagnosisCode.objects.get(id=self.diagnosisCode.id)
        self.assertEqual(diagnosisCode.abbreviated_description, "Abbr Desc 2")
        self.assertEqual(diagnosisCode.code, "A55")

    def test_diagnosisCode_update_Invalid_data_PUT(self):
        diagnosisCode = DiagnosisCode.objects.get(id=self.diagnosisCode.id)
        self.assertEqual(diagnosisCode.abbreviated_description, "Abbr Desc")
        self.assertEqual(diagnosisCode.code, "1123")

        req_body = {
            "category":"ABC", # It expects an integer
            "code":"A55",
            "abbreviated_description":"Abbr Desc 2",
            "full_description":"full Description 2"
        }
        response = self.client.put(f'{reverse(base_url)}{self.diagnosisCode.id}',req_body)

        # Checking status code of the request
        self.assertEqual(response.status_code, 400)


    # Testing the delete (DELETE) method and confirming that record was deleted
    def test_diagnosisCode_delete_DELETE(self):
        response = self.client.delete(f'{reverse(base_url)}{self.diagnosisCode.id}')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f'{reverse(base_url)}{self.diagnosisCode.id}')
        self.assertEqual(response.status_code, 404)

class TestDiagnosisCodePagination(APITestCase):
    def setUp(self):
        # Create a category object.
        self.category = Category.objects.create(code="A00", title="Cholera")

        # create 50 Diagnosis objects
        for count in range(50):
            DiagnosisCode.objects.create(
                category=self.category,
                code= f'AB{count}',
                abbreviated_description='Cholera due to Vibrio',
                full_description = 'Cholera due to Vibrio cholerae 01, biovar cholerae'
            )
            
    def test_pagination(self):
        response = self.client.get(reverse(base_url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 50)
        self.assertEqual(len(response.data['results']), 20)
        self.assertEqual(response.data['previous'], None)
        self.assertNotEqual(response.data['next'], None)
    
    def test_pagination_max_limit(self):
        limit_offset = {'limit':25, 'offset':10}
        url = f"{reverse('diagnosis-list')}?{urlencode(limit_offset)}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 25)  # Max length can't exceed 25
        self.assertNotEqual(response.data['previous'], None)
        self.assertNotEqual(response.data['next'], None)

class TestFileUpload(APITestCase):
    def setUp(self):
    # Create a category object.
        self.category = Category.objects.create(code="A00", title="Cholera")


    def test_file_upload(self):
        with open(f"{BASE_DIR}/static/test.csv", 'rb') as file:
            diagnosis_codes = DiagnosisCode.objects.all()
            self.assertEqual(diagnosis_codes.count(), 0)
            response = self.client.post(reverse('upload_csv'), {'email':'enninfrancis47@gmail.com','file':file}, format='multipart')
            self.assertEqual(response.status_code, 200)

class TestCategory(APITestCase):
    def setUp(self):
    # Create a category object.
        self.category = Category.objects.create(code="A00", title="Cholera")

        # create 50 Diagnosis objects
        for count in range(50):
            Category.objects.create(
                code=f"AA{count}",
                title=f"Category {count}"
            )
    
    def test_category_list(self):
        response = self.client.get(reverse(category_list))
        self.assertEqual(response.status_code, 200)

    def test_category_retrieve(self):
        response = self.client.get(reverse(category_detail, args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['code'], self.category.code)