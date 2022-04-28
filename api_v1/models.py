from django.db import models


class Category(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    

class DiagnosisCode(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='diagnose_codes')
    code = models.CharField(max_length=10)
    full_code = models.CharField(max_length=20, null=True, blank=True)
    abbreviated_description = models.TextField(null=True, blank=True)
    full_description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_code = self.category.code + self.code
        super(DiagnosisCode, self).save(*args, **kwargs)

    def __str__(self):
        return self.code
        

    
