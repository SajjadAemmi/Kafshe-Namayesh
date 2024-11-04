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


@csrf_protect
def b2(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        joined_date = request.POST.get('joined_date')
        new_member = Member(firstname=firstname, lastname=lastname, phone=phone, joined_date=joined_date)
        new_member.save()

        mymembers = Member.objects.all().values()
        template = loader.get_template('all_members.html')
        context = {
            'mymembers': mymembers,
        }
        return HttpResponse(template.render(context, request))


def testing(request):
    mydata = Member.objects.filter(firstname='Emil').values() | Member.objects.filter(
        firstname='Tobias').values()
    template = loader.get_template('template.html')
    context = {
        'mymembers': mydata,
        'fruits': ['Apple', 'Banana', 'Cherry'],
        'firstname': 'Linus',
    }
    return HttpResponse(template.render(context, request))
