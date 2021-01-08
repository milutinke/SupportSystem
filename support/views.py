from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from . import forms

User = get_user_model()


# Create your views here.
def index(request):
    return render(request, 'support/index.html', {'request': request})


def register_view(request):
    if request.method == 'POST':
        form = forms.RegisterFrom(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            country = form.cleaned_data.get('country')
            password = form.cleaned_data.get('password')
            password_confirmation = form.cleaned_data.get('password_confirmation')

            try:
                user = User.object.create_user(email, first_name, last_name, country, password, False)
            except:
                user = None

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                request.session['register_error'] = 1
    else:
        form = forms.RegisterFrom()

    return render(request, 'registration/registration.html', {'form': form})


def login_view(request):
    form = forms.LoginForm(request or None)

    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            request.session['invalid_user'] = 1

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)

    return render(request, 'logout.html')