from rest_framework.test import APITestCase,APIClient
from api_v1.models import DiagnosisCode, Category


class TestViewTestCase(APITestCase):
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
        


    ######################################################
    # This is the Test for the GET ( list ) method, the  #
    # method to retrieve and diagnosisCode paginated 20  #
    # records per request                                #
    ######################################################
    def test_diagnosisCode_list_GET(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']),1)

    def test_diagnosisCode_list_Check_Pagination_GET(self):
        DiagnosisCode.objects.create(
            category = self.category,
            code="1213",
            abbreviated_description="Abbr Desc",
            full_description="full Description"
        )
        DiagnosisCode.objects.create(
            category = self.category,
            code="1123",
            abbreviated_description="Abbr Desc 22",
            full_description="full Description22"
        )
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']),3)
        self.assertEqual(response.json()['count'],3)

    # Testing the create(POST) method with data in the body of the request
    def test_diagnosisCode_create_POST(self):
        req_body = {
            "category":self.category.id,
            "code":"2212",
            "abbreviated_description":"Abbr Desc 2",
            "full_description":"full Description 2"
        } 
        response = self.client.post(self.base_url, req_body)
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
        response = self.client.post(self.base_url, req_body)
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

    # Testing the partial update (PATCH) method
    def test_diagnosisCode_update_PATCH(self):

        diagnosisCode = DiagnosisCode.objects.get(id=self.diagnosisCode.id)

        self.assertEqual(diagnosisCode.abbreviated_description, "Abbr Desc")
        self.assertEqual(diagnosisCode.code, "1123")

        req_body = {
            "abbreviated_description":"New Desc",
            "code":"2"
        }
        response = self.client.patch(self.base_url + f'{self.diagnosisCode.id}',req_body)

        # Checking status code of the request
        self.assertEqual(response.status_code, 200)
        # confirming that object was updated
        diagnosisCode = DiagnosisCode.objects.get(id=self.diagnosisCode.id)
        self.assertEqual(diagnosisCode.abbreviated_description, "New Desc")
        self.assertEqual(diagnosisCode.code, "2")

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
        response = self.client.put(self.base_url + f'{self.diagnosisCode.id}',req_body)

        # Checking status code of the request
        self.assertEqual(response.status_code, 200)
        # confirming that object was updated
        diagnosisCode = DiagnosisCode.objects.get(id=self.diagnosisCode.id)
        self.assertEqual(diagnosisCode.abbreviated_description, "Abbr Desc 2")
        self.assertEqual(diagnosisCode.code, "A55")

    # Testing the retrieve (GET) method and confirming that it return the correct data
    def test_diagnosisCode_retrieve_GET(self):
        response = self.client.get(self.base_url + f'{self.diagnosisCode.id}')

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['id'],self.diagnosisCode.id)

    # Testing the delete (DELETE) method and confirming that record was deleted
    def test_diagnosisCode_delete_DELETE(self):
        response = self.client.delete(self.base_url + f'{self.diagnosisCode.id}')
        self.assertEqual(response.status_code, 204)

        response = self.client.get(self.base_url + f'{self.diagnosisCode.id}')
        self.assertEqual(response.status_code, 404)

