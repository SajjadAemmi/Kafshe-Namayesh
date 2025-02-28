from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from shop.models import Shoe, Member, Order, Cart, CartItem
from shop.cart import add_to_cart, remove_from_cart, get_cart_items, get_cart_total
from shop.orders import create_order


# Create your views here.

def index(request):
    shoes = Shoe.objects.prefetch_related('images').all()
    return render(request, 'index.html', {
        "shoes": shoes
    })


def products(request):
    shoes = Shoe.objects.prefetch_related('images', 'comments').all()
    template = loader.get_template('products.html')
    context = {
        'shoes': shoes,
    }
    return HttpResponse(template.render(context, request))


def products_by_type(request, shoe_type):
    SHOE_TYPES_DICT = {
        'kids': 'بچگانه',
        'women': 'زنانه',
        'men': 'مردانه',
    }

    if shoe_type not in SHOE_TYPES_DICT:
        return render(request, '404.html', status=404)  # Show a 404 page if type is invalid

    shoes = Shoe.objects.filter(type=shoe_type)
    return render(request, 'products.html', {'shoes': shoes, 'shoe_type': SHOE_TYPES_DICT[shoe_type]})


def product(request, id):
    shoe = get_object_or_404(Shoe.objects.prefetch_related('images', 'comments'), id=id)
    template = loader.get_template('product.html')
    context = {
        'shoe': shoe,
    }
    return HttpResponse(template.render(context, request))


def add_to_cart(request, shoe_id):
    # Get the shoe object or return 404 if not found
    shoe = get_object_or_404(Shoe, id=shoe_id)

    # Implement logic to add shoe to the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Create or update CartItem for the shoe
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, shoe=shoe)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')


def cart_remove(request, shoe_id):
    remove_from_cart(request, shoe_id)
    return redirect('cart_detail')


def cart_detail(request):
    cart_items = get_cart_items(request.user)
    cart_total = get_cart_total(request.user)
    return render(request, 'cart_detail.html',
                  {
                      'cart_items': cart_items,
                      'cart_total': cart_total
                  })


@login_required
def order_create(request):
    """Create a new order from the cart and clear the cart."""
    order = create_order(request.user)
    request.session['cart'] = {}  # Clear the cart session
    return redirect('order_detail', order_id=order.id)


@login_required
def order_detail(request, order_id):
    """Display the details of a specific order."""
    order = Order.objects.get(id=order_id, user=request.user)


def members(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template('all_members.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')