from django.db import models
from django.conf import settings


# Create your models here.
class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Shoe(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    joined_date = models.DateField(null=True)

    def __str__(self):
        return self.name


class ShoeImage(models.Model):
    shoe = models.ForeignKey(Shoe, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shoe_images/')  # Adjust the path as needed

    def __str__(self):
        return f"Image for {self.shoe.name}"


class Comment(models.Model):
    shoe = models.ForeignKey(Shoe, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference to the user model
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.shoe.name}"
