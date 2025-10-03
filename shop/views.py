from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from shop.models import Shoe, Member, Order, OrderItem, Cart, CartItem
from shop.cart import add_to_cart, remove_from_cart, get_cart_items, get_cart_total, get_or_create_cart
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
    shoe = get_object_or_404(Shoe, id=shoe_id)
    cart, created = get_or_create_cart(request.user, request.session)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, shoe=shoe)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def remove_from_cart(request, shoe_id):
    cart, _ = get_or_create_cart(request.user, request.session)  # ← اضافه شد session

    # پیدا کردن آیتم سبد برای محصول مشخص
    cart_item = CartItem.objects.filter(cart=cart, shoe_id=shoe_id).first()
    if cart_item:
        cart_item.delete()  # حذف آیتم

    return redirect('cart')  # بازگشت به صفحه سبد خرید


def cart(request):
    cart, created = get_or_create_cart(request.user, request.session)
    cart_items = cart.items.all()
    cart_total = sum(item.get_total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})


@login_required(login_url='/accounts/login/')
def checkout(request):
    cart, created = get_or_create_cart(request.user, request.session)

    if not cart.items.exists():
        return redirect('cart')  # اگر سبد خالی بود برگرده

    # ساخت سفارش
    order = Order.objects.create(user=request.user if request.user.is_authenticated else None)

    total_price = 0
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            shoe=item.shoe,
            quantity=item.quantity
        )
        total_price += item.get_total_price()

    order.total_price = total_price
    order.save()

    cart_items = cart.items.all()
    cart_total = sum(item.get_total_price() for item in cart_items)

    # پاک کردن سبد خرید
    # cart.items.all().delete()

    return render(request, 'checkout.html', {'order': order, 'cart_total': cart_total})

@login_required
def order_create(request):
    """Create a new order from the cart and clear the cart."""
    order = create_order(request.user)
    request.session['cart'] = {}  # Clear the cart session
    return redirect('order_detail', order_id=order.id)


@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'checkout.html', {'order': order})


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


@login_required
def profile(request):
    return render(request, "user/profile.html", {"user": request.user})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")  # بعد از ثبت نام به صفحه اصلی برو
        else:
            print(form.errors)  # برای دیدن خطاها در کنسول
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def order_list(request):
    orders = request.user.orders.prefetch_related("items__shoe").all().order_by("-created_at")
    return render(request, "user/orders.html", {"orders": orders})
