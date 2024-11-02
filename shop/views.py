from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from shop.models import Shoe, Member


def index(request):
    images = [1, 2, 3, 4]
    return render(request, 'index.html', {
        "images": images
    })


# Create your views here.
def details(request, id):
    mymember = Shoe.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'mymember': mymember,
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
