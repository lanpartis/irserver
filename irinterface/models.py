from django.db import models

# Create your models here.
class PdImage(models.Model):
    '''Predicted image. Image and class predictions'''
    image_src = models.ImageField(upload_to='img')
    model_name = models.CharField(max_length=20)
    prediction = models.CharField(max_length=200)

    prediction1 = models.CharField(max_length=200)
    prediction2 = models.CharField(max_length=200)
    prediction3 = models.CharField(max_length=200)
    prediction4 = models.CharField(max_length=200)

class PdModel(models.Model):
    model_src = models.FileField(upload_to='upload_networks')
    # weights_src = models.FileField(upload_to='upload_networks')
