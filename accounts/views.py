from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404

from .forms import CustomUserCreationForm
from .models import CustomUser
from main.models import Article


def index(request):
    users = CustomUser.objects.all()
    return render(request, 'accounts/index.html', {'users': users})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile', user.id)
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def profile_view(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    article_list = Article.objects.filter(author__user__id=user.id)
    return render(request, 'accounts/profile.html', {'user':user, 'article_list': article_list,})
