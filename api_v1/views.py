# Importing from external libraries
import csv
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status

# Local imports
from api_v1.models import DiagnosisCode, Category
from api_v1 import serializers as srz
from api_v1.utils import check_is_CSV, process_file
from .tasks import create_diagnosis_codes_async_task



# CRUD Operations ViewSet For Category Records
class CategoryViewSet(ModelViewSet):
    serializer_class = srz.CategorySerializer
    queryset = Category.objects.all()

# CRUD Operations ViewSet For Diagnosis Code Records
class DiagnosisCodeViewSet(ModelViewSet):
    serializer_class = srz.DiagnosisCodeSerializer
    queryset = DiagnosisCode.objects.all()




# File upload to create Diagnosis code records
class UploadCSVFileView(APIView):
    serializer_class = srz.UploadCSVFileSerializer

    def post(self, request):
        # Validate received data
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        # Checking the extension of the uploaded file (if it is a csv file)
        is_csv = check_is_CSV(data.validated_data.get('file').content_type)
        
        if is_csv:

            file_content = process_file(data.validated_data.get('file'))
            create_diagnosis_codes_async_task.delay(file_content,data.validated_data.get('email'))
            return Response({
                "message":"Data upload is successful"
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "detail":"File is not CSV type"
                }, status=status.HTTP_400_BAD_REQUEST
            )