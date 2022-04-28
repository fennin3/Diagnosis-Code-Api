from django.urls import path, include
from rest_framework import routers
from api_v1.views import CategoryViewSet,DiagnosisCodeViewSet,UploadCSVFileView


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'', DiagnosisCodeViewSet, basename='diagnosis')

urlpatterns = [
    path('upload',UploadCSVFileView.as_view(), name="upload_csv"),
    path('', include(router.urls)),
]

