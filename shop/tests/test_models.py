# shop/tests/test_models.py
from django.test import TestCase
from shop.models import Shoe

class ShoeModelTest(TestCase):
    def test_str_returns_name(self):
        shoe = Shoe.objects.create(name="Sample Shoe", price=100, created_date="2025-11-01")
        self.assertEqual(str(shoe), "Sample Shoe")
