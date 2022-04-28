# Generated by Django 3.2.11 on 2022-04-28 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0002_rename_diagnosis_code_diagnosiscode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosiscode',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnose_codes', to='api_v1.category'),
        ),
        migrations.AlterField(
            model_name='diagnosiscode',
            name='full_code',
            field=models.CharField(max_length=20),
        ),
    ]