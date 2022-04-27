from django.urls import path, include
from rest_framework import routers
from api_v1.views import DiagnosisCodeViewSet


router = routers.DefaultRouter(trailing_slash=False)

router.register(r'', DiagnosisCodeViewSet, 'diagnosis')

urlpatterns = [
    path('', include(router.urls)),
]

