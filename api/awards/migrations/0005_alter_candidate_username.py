# Generated by Django 5.1.4 on 2024-12-25 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0004_alter_candidate_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
