from django.shortcuts import render
from basic_password_auth_app.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
    return render(request, 'basic_password_auth_app/index.html')


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        user_profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile = user_profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                print(request.FILES['profile_pic'])
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, user_profile_form.errors)
    else:
        user_form = UserForm()
        user_profile_form = UserProfileInfoForm()

    return render(request, 'basic_password_auth_app/register.html', context={'registered': registered,
                                                                             'user_form': user_form,
                                                                             'user_profile_form': user_profile_form})


def user_login(request):
    if request.method == "POST":
        print('User has filled the login information and submitted')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Your account is cuurently InActive')
        else:
            print('Authentication Failure for : {}, {}'.format(username, password))
            return HttpResponse('Authentication Failure!!')
    else:
        return render(request, 'basic_password_auth_app/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
