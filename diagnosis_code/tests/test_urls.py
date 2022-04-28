from django.test import SimpleTestCase
from django.urls import resolve, reverse

from diagnosis_code.views import DiagnosisCodeViewSet, CategoryViewSet

class TestDiagnosisUrls(SimpleTestCase):
    
    def test_diagnosis_list_create_url_resolves_diagnosislistview(self):
        view = resolve('/api/v1/diagnosis-codes')
        self.assertEqual(view.func.__name__, DiagnosisCodeViewSet.__name__)
        
    def test_diagnosis_detail_url_resolves_diagnosisdetailview(self):
        view = resolve('/api/v1/diagnosis-codes/1')
        self.assertEqual(view.func.__name__, DiagnosisCodeViewSet.__name__)

    def category_list_create_url_resolves_categorylistview(self):
        view = resolve('/api/v1/categories')
        self.assertEqual(view.func.__name__, CategoryViewSet.__name__)


    def category_detail_url_resolves_categorydetailview(self):
        view = resolve('/api/v1/diagnosis-codes/1')
        self.assertEqual(view.func.__name__, CategoryViewSet.__name__)