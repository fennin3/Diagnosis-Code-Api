# Importing from external libraries
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status

# Local imports
from api_v1.models import DiagnosisCode
from api_v1.serializers import DiagnosisCodeSerializer, UploadCSVFileSerializer
from api_v1.utils import check_is_CSV, create_diagnosis_code_from_csv



# CRUD Operations ViewSet For Diagnosis Code Records
class DiagnosisCodeViewSet(ModelViewSet):
    serializer_class = DiagnosisCodeSerializer
    queryset = DiagnosisCode.objects.all()


# File upload to create Diagnosis code records
class UploadCSVFileView(APIView):
    serializer_class = UploadCSVFileSerializer

    def post(self, request):
        # Validate received data
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        # Checking the extension of the uploaded file (if it is a csv file)
        is_csv = check_is_CSV(data.validated_data.get('file').content_type)

        if is_csv:
            success = create_diagnosis_code_from_csv(data.validated_data.get('file'))
            return Response()
        else:
            return Response(
                {
                    "detail":"File is not CSV type"
                }, status=status.HTTP_417_EXPECTATION_FAILED
            )