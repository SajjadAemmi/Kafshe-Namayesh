from .models import Order, OrderItem
from .cart import get_cart_items, get_cart_total, get_or_create_cart

def create_order(user):
    """Create an order from the user's cart."""
    cart_items = get_cart_items(user)
    order = Order.objects.create(user=user, status='pending')

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            shoe=item.shoe,
            quantity=item.quantity
        )

    return order
