from django.urls import path, include
from rest_framework import routers
from diagnosis_code.views import CategoryViewSet,DiagnosisCodeViewSet,UploadCSVFileView


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'diagnosis-codes', DiagnosisCodeViewSet, basename='diagnosis')

urlpatterns = [
    path('upload',UploadCSVFileView.as_view(), name="upload_csv"),
    path('v1/', include(router.urls)), #urls for viewsets
]

