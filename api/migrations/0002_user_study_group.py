# Generated by Django 5.0.6 on 2024-06-06 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='study_group',
            field=models.CharField(max_length=50, null=True),
        ),
    ]