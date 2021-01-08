from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from . import forms
from .models import Ticket, TicketAnswers
from django.http import HttpResponse

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
                request.session['error'] = 'Registration error!'
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
            request.session['error'] = 'Invalid user!'

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)

    return render(request, 'logout.html')


def tickets(request):
    if not request.user.is_authenticated:
        request.session['error'] = 'You must be logged in to see this!'
        return redirect('/')

    try:
        tickets_ = Ticket.objects.filter(user_id=request.user.id)
    except Ticket.DoesNotExist:
        tickets_ = None

    return render(request, 'support/tickets.html', {'tickets': tickets_})


def ticket(request, ticket_id):
    if not request.user.is_authenticated:
        request.session['error'] = 'You must be logged in to see this!'
        return redirect('/')

    try:
        ticket_ = Ticket.objects.get(id=ticket_id)

        if ticket_.user.id != request.user.id:
            request.session['error'] = 'Action forbidden!'
            return redirect('/')

    except Ticket.DoesNotExist:
        request.session['error'] = 'Invalid ticket!'
        return redirect('/')

    if request.method == 'POST':
        form = forms.AnswerTicketForm(data=request.POST)

        if form.is_valid():
            content = form.cleaned_data.get('content')
            answer = TicketAnswers(content=content, user=request.user, ticket=ticket_)
            answer.save()

        return redirect('/tickets/' + ticket_id.__str__())
    else:
        form = forms.AnswerTicketForm(None)

    try:
        answers = TicketAnswers.objects.filter(ticket_id=ticket_id)
    except TicketAnswers.DoesNotExist:
        answers = None

    context = {
        'ticket': ticket_,
        'answers': answers,
        'form': form
    }

    return render(request, 'support/ticket.html', context)
