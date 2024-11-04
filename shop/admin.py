from django.contrib import admin
from django.utils.html import format_html, format_html_join
from .models import Shoe, ShoeImage, Comment, Cart, CartItem, Order, OrderItem


# Register your models here.

class ShoeImageInline(admin.TabularInline):
    model = ShoeImage
    extra = 1


class ShoeAdmin(admin.ModelAdmin):
    inlines = [ShoeImageInline]  # Add other inlines as necessary
    list_display = ('name', 'price')

    # Add custom field to display comments
    readonly_fields = ('comments_display',)

    def comments_display(self, obj):
        comments = obj.comments.all()
        if comments.exists():
            # Format each comment with user and created date
            return format_html_join(
                '',  # No separator
                '<p><strong>{}</strong> ({}):<br>{}</p>',
                ((comment.user.username, comment.created_at.strftime('%Y-%m-%d %H:%M'), comment.text) for comment in
                 comments)
            )
        return "No comments yet."

    comments_display.short_description = "Comments"  # Field label in the admin


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('shoe', 'quantity', 'get_total_price')

    def get_total_price(self, obj):
        return obj.get_total_price()

    get_total_price.short_description = 'Total Price'


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'get_total_price')
    readonly_fields = ('user', 'created_at', 'get_total_price')
    inlines = [CartItemInline]

    def get_total_price(self, obj):
        return obj.get_total_price()

    get_total_price.short_description = 'Total Cart Price'


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'shoe', 'quantity', 'get_total_price')
    readonly_fields = ('cart', 'shoe', 'quantity', 'get_total_price')

    def get_total_price(self, obj):
        return obj.get_total_price()

    get_total_price.short_description = 'Total Price'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('shoe', 'quantity', 'get_total_price')

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Price'

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'get_total_price')
    list_filter = ('status', 'created_at')
    readonly_fields = ('user', 'created_at', 'get_total_price')
    inlines = [OrderItemInline]

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Total Order Price'

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Shoe, ShoeAdmin)
admin.site.register(Comment)
