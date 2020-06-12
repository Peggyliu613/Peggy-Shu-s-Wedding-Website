from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'index.html')

def add_guest(request):
    is_shu_friend_relative = False
    if request.POST.get('is_shu_friend_relative'):
        is_shu_friend_relative = True
    is_peggy_friend_relative = False
    if request.POST.get('is_peggy_friend_relative'):
        is_peggy_friend_relative = True
    
    errors=Guest.objects.validator(
        request.POST, is_shu_friend_relative, is_peggy_friend_relative)

    if errors:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/#rsvp')

    diet_restriction = 'none'
    other_diet_message = ''
    if request.POST.get('diet_restriction'):
        diet_restriction = request.POST['diet_restriction']
        if diet_restriction == 'others':
            other_diet_message = request.POST['other']
    
    message = ''
    if request.POST.get('message'):
        message = request.POST['message']
    
    print(message)

    full_name=request.POST['full_name']
    email=request.POST['email']
    number_of_guests=int(request.POST['number_of_guests'])
    
    Guest.objects.create(
        full_name=full_name, email=email, is_shu_friend_relative=is_shu_friend_relative,
        is_peggy_friend_relative=is_peggy_friend_relative,
        number_of_guests=number_of_guests, diet_restriction=diet_restriction,
        diet_message=other_diet_message, message=message)
    return redirect('/submited')

def submited(request):
    return render(request, 'submited.html')

def see_guest(request):
    if 'user' not in request.session or request.session['user'] != 1:
       return redirect('/')
    else:
        context = {
            "all_guests":Guest.objects.all(),
        }
        return render(request, 'guest.html', context)

def register(request):
    return render(request, 'register.html')

def register_now(request):
    errors=User.objects.validator(request.POST)

    if errors:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/register')
    else:
        u=request.POST['user_name']
        p=request.POST['password']
        p_hash= bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()
        User.objects.create(user_name=u, password=p_hash)
    return redirect('/')

def login(request):
    return render(request, 'login.html')

def login_now(request):
    if not request.POST['user_name']:
        return redirect('/')

    errors=User.objects.validator_login(request.POST)
    if errors:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/login')
    
    user=User.objects.get(user_name=request.POST['user_name'])
    request.session['user']=user.id
    return redirect('/see_guest')

def logout(request):
    request.session['user']=None
    return redirect('/')

def erase_guest(request):
    c=Guest.objects.get(email=request.POST['delete'])
    c.delete()
    return redirect('/see_guest')