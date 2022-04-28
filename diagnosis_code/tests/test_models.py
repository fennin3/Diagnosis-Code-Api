from django.test import TestCase
from diagnosis_code.models import Category, DiagnosisCode

class DiagnosisCategoryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create Diagnosis Category object
        Category.objects.create(code="A00", title="Cholera")

    def test_diagnosis_details(self):
        category = Category.objects.get(id=1)
        category_code = f'{category.code}'
        category_title = f'{category.title}'
        self.assertEqual(category_code, 'A00')
        self.assertEqual(category_title, 'Cholera')


class DiagnosisTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create Diagnosis Category object
        category = Category.objects.create(code="A00", title="Cholera")
        
        # create Diagnosis object
        DiagnosisCode.objects.create(category=category, code="1",
                                            abbreviated_description="Cholera, unspecified",
                                            full_description="Cholera due to Vibrio cholerae 01, biovar cholerae")

    def test_diagnosis_details(self):
        diagnosis = DiagnosisCode.objects.get(id=1)
        category = f'{diagnosis.category.code}'
        code = f'{diagnosis.code}'
        abbreviated_description = f'{diagnosis.abbreviated_description}'
        full_description = f'{diagnosis.full_description}'
        self.assertEqual(category, 'A00')
        self.assertEqual(code, '1')
        self.assertEqual(diagnosis.full_code, 'A001')
        self.assertEqual(abbreviated_description, 'Cholera, unspecified')
        self.assertEqual(full_description,'Cholera due to Vibrio cholerae 01, biovar cholerae')