from django.db import models


class Shoe(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    joined_date = models.DateField(null=True)

    def __str__(self):
        return self.name
