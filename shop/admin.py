from django.contrib import admin

# Register your models here.
from .models import Shoe, ShoeImage

class ShoeImageInline(admin.TabularInline):
    model = ShoeImage
    extra = 1

class ShoeAdmin(admin.ModelAdmin):
    inlines = [ShoeImageInline]

admin.site.register(Shoe, ShoeAdmin)