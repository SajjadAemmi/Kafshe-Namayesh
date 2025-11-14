from django.contrib.sitemaps import Sitemap
from .models import Shoe
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return ['index', 'about', 'contact']  # example static pages

    def location(self, item):
        return reverse(item)


class ShoeSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Shoe.objects.all()

    def lastmod(self, obj):
        return obj.created_date

    def location(self, obj):
        # Use ID instead of slug
        return f"/products/{obj.id}/"
