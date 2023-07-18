from django.db import models
from django.contrib.auth.models import User

# Create your models here.

    
class File(models.Model):
    FILE_TYPES = (
        ('pdf', 'PDF'),
        ('txt', 'Text File'),
        ('doc', 'Word Document'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    file_type = models.CharField(max_length=10, choices=FILE_TYPES, default='pdf')
    file = models.FileField(upload_to='files/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0)
    email_count = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return self.title
    