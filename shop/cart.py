from .models import Cart, CartItem, Shoe

def get_or_create_cart(user=None):
    """Retrieve or create a cart for the user (or a guest cart if user is None)."""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

def add_to_cart(user, shoe_id, quantity=1):
    """Add a shoe to the user's cart or update its quantity."""
    cart = get_or_create_cart(user)
    shoe = Shoe.objects.get(id=shoe_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, shoe=shoe)
    if not created:
        cart_item.quantity += quantity
    cart_item.save()

def remove_from_cart(user, shoe_id):
    """Remove a shoe from the cart."""
    cart = get_or_create_cart(user)
    CartItem.objects.filter(cart=cart, shoe_id=shoe_id).delete()

def get_cart_items(user):
    """Retrieve all items in the user's cart."""
    cart = get_or_create_cart(user)
    return cart.items.all()

def get_cart_total(user):
    """Calculate the total cost of the cart."""
    cart = get_or_create_cart(user)
    return cart.get_total_price()
