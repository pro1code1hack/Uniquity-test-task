from django.contrib.auth.models import AbstractUser, User
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .forms import LoginForm, UserRegistrationForm


def user_login(request):
    form = LoginForm(request.POST if request.method == 'POST' else None)
    if form.is_valid():
        cd = form.cleaned_data
        user: AbstractUser = authenticate(request, email=cd['email'], password=cd['password'])
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('Invalid login')
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                error = 'User already exists!'
                return render(request, 'account/register.html', {'register_form': form, 'error': error})

            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return HttpResponseRedirect('/')
    else:
        form = UserRegistrationForm()

    return render(request, 'account/register.html', {'register_form': form})

