from rest_framework.viewsets import ModelViewSet
from api_v1.models import DiagnosisCode
from api_v1.serializers import DiagnosisCodeSerializer




class DiagnosisCodeViewSet(ModelViewSet):
    serializer_class = DiagnosisCodeSerializer
    queryset = DiagnosisCode.objects.all()