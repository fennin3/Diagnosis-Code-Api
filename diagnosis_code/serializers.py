from rest_framework import serializers
from .models import Category, DiagnosisCode

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields='__all__'


class DiagnosisCodeSerializer(serializers.ModelSerializer):
    full_code = serializers.CharField(read_only=True)
    class Meta:
        model = DiagnosisCode
        fields = '__all__'


class UploadCSVFileSerializer(serializers.Serializer):
    email = serializers.EmailField()
    file = serializers.FileField()

