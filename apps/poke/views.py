from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.db.models import Count
from django.contrib.messages import error


# Create your views here.

def index(request):
    return render(request,'poke/index.html')


def create(request):
    errors= User.objects.validate_registration(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    else:
        user = User.objects.valid_user(request.POST)
        request.session['user_id'] = user.id
        #keeps track of the current user_id that is "logged in", 
        # you can directly use it as argument, no need to pass into parameters: def example(x,y):
        messages.success(request, "registered")
        return redirect ('/success')






def login(request):
    errors= User.objects.validate_login(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    else:
        user = User.objects.valid_login(request.POST)
        request.session['user_id'] = user.id
        messages.success(request, "Logged in")
        return redirect('/success')



def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'poke/success.html', context)




def logout(request):
    context = {
        'logout': request.session.pop('user_id')
    }
    return render(request,'poke/index.html', context)


################  END END LOGIN END END  ################################################################################

#poker = Fk; rn = poking

#poked_by = Fk; rn = poked


def home(request):
    logged_user = User.objects.get(id=request.session['user_id'])

    context = {
        "pokez": Poke.objects.all(),
        "poke_count": Poke.objects.filter(poked_by = logged_user),
        "poke_total": Poke.objects.filter(poked_by = logged_user).values('poker').annotate(Count('poker')),
        "current": User.objects.get(id=request.session['user_id']),
        "others": User.objects.exclude(id=request.session['user_id']),
    }
    return render(request, 'poke/home.html', context)


def poke_process(request):
    poker_id = User.objects.get(id=request.POST['poker_id'])
    poked_by_id = User.objects.get(id=request.POST['poked_by_id'])

    poke_process = Poke.objects.create(poker = poker_id, poked_by = poked_by_id)

    return redirect('/home')


#poker = Fk; rn = poking

#poked_by = Fk; rn = poked