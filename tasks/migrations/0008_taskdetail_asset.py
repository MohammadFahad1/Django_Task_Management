# Generated by Django 5.1.6 on 2025-04-02 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_delete_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskdetail',
            name='asset',
            field=models.ImageField(blank=True, null=True, upload_to='tasks_assets'),
        ),
    ]
