# Generated by Django 4.2.3 on 2023-07-17 23:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('file_type', models.CharField(choices=[('pdf', 'PDF'), ('txt', 'Text File'), ('doc', 'Word Document'), ('image', 'Image'), ('audio', 'Audio'), ('video', 'Video')], default='pdf', max_length=10)),
                ('file', models.FileField(upload_to='files/')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('download_count', models.PositiveIntegerField(default=0)),
                ('email_count', models.PositiveIntegerField(default=0)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
