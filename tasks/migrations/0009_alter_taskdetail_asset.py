# Generated by Django 5.1.6 on 2025-04-02 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_taskdetail_asset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdetail',
            name='asset',
            field=models.ImageField(blank=True, default='task_assets/default_image.png', null=True, upload_to='tasks_assets'),
        ),
    ]
