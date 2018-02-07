from django.db import models

# Create your models here.
class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    docID = models.CharField(max_length=10,)