from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as django_login
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def admin_register(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                user.is_superuser = True
                user.is_staff = True
                user.save()
                return redirect('/admin/')
        else:
            form = UserCreationForm()
        return render(request, 'admin_register.html', {'form': form})
    else:
        return HttpResponse('<h1>Você não tem autorização para  visualizar esta página</h1>',
                            status=401)

@require_http_methods(["GET", "POST"])
def login(request):
        if request.method == 'POST':
            form = AuthenticationForm(data = request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                django_login(request, user)
                if user.is_superuser:
                    return redirect('/admin/') 
                else:
                    return redirect('/dicionario/')
        else:
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    return redirect('/admin/')
                else:
                    return redirect('/dicionario/')
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})