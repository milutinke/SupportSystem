from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterFrom(forms.Form):
    email = forms.EmailField(label='E-Mail', required=True, max_length=255)
    first_name = forms.CharField(label='First Name', required=True, max_length=64)
    last_name = forms.CharField(label='Last Name', required=True, max_length=64)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'id': 'confirm'
    }))

    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'id': 'password_confirm'
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        result = User.object.filter(email__iexact=email)

        if result.exists():
            raise forms.ValidationError('This email is alerady in use!')

        return email


class LoginForm(forms.Form):
    email = forms.EmailField(label='E-Mail')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password'
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        result = User.object.filter(email__iexact=email)

        if not result.exists():
            raise forms.ValidationError('The account with provided email does not exists!')

        return email


class CreateTicketFrom(forms.Form):
    email = forms.EmailField(label='E-Mail', required=True)
    password = forms.CharField(widget=forms.PasswordInput)


class CreateTicketFrom(forms.Form):
    title = forms.CharField(max_length=96, required=True)
    product = forms.CharField(max_length=128, required=True)
    content = forms.CharField(widget=forms.Textarea, max_length=2048, required=True)


class ReplyTicketForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, max_length=2048, required=True)
