from django.test import SimpleTestCase
from django.urls import resolve, reverse

from api_v1.views import DiagnosisCodeViewSet

class TestDiagnosisUrls(SimpleTestCase):
    
    def test_diagnosis_list_create_url_resolves_diagnosislistview(self):
        view = resolve('/api/v1/codes/')
        self.assertEqual(view.func.__name__, DiagnosisCodeViewSet.__name__)
        
    def test_diagnosis_detail_url_resolves_diagnosislistview(self):
        view = resolve('/api/v1/codes/1')
        self.assertEqual(view.func.__name__, DiagnosisCodeViewSet.__name__)