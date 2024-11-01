from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.middleware import csrf
from django.views.decorators.csrf import csrf_protect
from shop.models import shoe


def members(request):
    mymembers = models.Member.objects.all().values()
    template = loader.get_template('all_members.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))


def b(request):
    csrf_token = csrf.get_token(request)
    template = loader.get_template('d.html')
    context = {
        'csrf_token': csrf_token,
    }
    return HttpResponse(template.render(context, request))


@csrf_protect
def b2(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        joined_date = request.POST.get('joined_date')
        new_member = models.Member(firstname=firstname, lastname=lastname, phone=phone, joined_date=joined_date)
        new_member.save()
        
        mymembers = models.Member.objects.all().values()
        template = loader.get_template('all_members.html')
        context = {
            'mymembers': mymembers,
        }
        return HttpResponse(template.render(context, request))


def details(request, id):
    mymember = shoe.Shoe.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'mymember': mymember,
    }
    return HttpResponse(template.render(context, request))


def index(request):
    images = [1, 2, 3, 4]
    return render(request, 'index.html', {
        "images": images
    })


def testing(request):
    mydata = models.Member.objects.filter(firstname='Emil').values() | models.Member.objects.filter(firstname='Tobias').values()
    template = loader.get_template('template.html')
    context = {
        'mymembers': mydata,
        'fruits': ['Apple', 'Banana', 'Cherry'],
        'firstname': 'Linus',
    }
    return HttpResponse(template.render(context, request))
