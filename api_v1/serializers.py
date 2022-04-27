from rest_framework import serializers
from .models import Category, DiagnosisCode

class CategoryCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields='__all__'


class DiagnosisCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisCode
        fields = '__all__'


class UploadCSVFileSerializer(serializers.Serializer):
    email = serializers.EmailField()
    file = serializers.FileField()

