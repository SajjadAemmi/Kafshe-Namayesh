from .models import Cart, CartItem, Shoe

def get_or_create_cart(user, session):
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user)
    else:
        cart_id = session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id=cart_id, user=None).first()
            if not cart:
                cart = Cart.objects.create(user=None)
                session['cart_id'] = cart.id
        else:
            cart = Cart.objects.create(user=None)
            session['cart_id'] = cart.id
        created = False
    return cart, created


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

def get_cart_items(user, session):
    cart, _ = get_or_create_cart(user, session)
    return cart.items.all()

def get_cart_total(user, session):
    cart, _ = get_or_create_cart(user, session)
    return sum(item.get_total_price() for item in cart.items.all())
