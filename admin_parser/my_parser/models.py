from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(verbose_name='Title', max_length=20)
    price = models.CharField(
        verbose_name='Price',
        max_length=50
    )
    currency = models.CharField(max_length=10)
    date = models.DateTimeField()
    url = models.URLField(unique=True)

    def __str__(self):
        return self.title

