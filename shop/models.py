from datetime import date, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.

class Shoe(models.Model):
    SHOE_TYPES = [
        ('kids', 'بچگانه'),
        ('women', 'زنانه'),
        ('men', 'مردانه'),
    ]
    SHOE_CATEGORY = [
        ('loafer', 'راحتی'),
        ('sport', 'ورزشی'),
        ('boot', 'بوت'),
        ('sandal', 'صندل و تابستانی'),
        ('leather', 'چرمی'),
        ('classic', 'کلاسیک'),
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=SHOE_TYPES)
    category = models.CharField(max_length=10, choices=SHOE_CATEGORY, default='loafer')
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    created_date = models.DateField(null=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def is_new(self):
        """Return True if shoe was added within the last 30 days"""
        if not self.created_date:
            return False
        return (date.today() - self.created_date) <= timedelta(days=30)


class ShoeImage(models.Model):
    shoe = models.ForeignKey(Shoe, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shoe_images/')  # Adjust the path as needed

    def __str__(self):
        return f"Image for {self.shoe.name}"


class Comment(models.Model):
    shoe = models.ForeignKey(Shoe, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference to the user model
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)  # ⭐
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.shoe.name}"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.shoe.name}"

    def get_total_price(self):
        return self.shoe.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده، در حال پردازش'),
        ('shipped', 'در حال ارسال'),
        ('completed', 'انجام شده'),
        ('canceled', 'لغو شده'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.shoe.name}"

    def get_total_price(self):
        return self.shoe.price * self.quantity


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question