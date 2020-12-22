from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='classification_input')
    classification = models.IntegerField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'image'