from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from shop.models import Shoe, Member


def index(request):
    shoes = Shoe.objects.prefetch_related('images').all()
    return render(request, 'index.html', {
        "shoes": shoes
    })


# Create your views here.
def details(request, id):
    shoe = get_object_or_404(Shoe.objects.prefetch_related('images'), id=id)
    template = loader.get_template('details.html')
    context = {
        'shoe': shoe,
    }
    return HttpResponse(template.render(context, request))


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
