# Generated by Django 3.2.11 on 2022-04-28 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0003_auto_20220428_0242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosiscode',
            name='full_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
