from usuarios.models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomCreationForm(UserCreationForm):

    first_name = forms.CharField(required=True, label='Primeiro Nome')
    last_name = forms.CharField(required=True, label='Último Nome')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        self.fields['username'].widget = forms.TextInput(attrs={
            'placeholder': 'Digite seu nome'
        })

        self.fields['first_name'].widget = forms.TextInput(attrs={
            'placeholder': 'Digite seu primeiro nome'
        })

        self.fields['last_name'].widget = forms.TextInput(attrs={
            'placeholder': 'Digite seu ultimo nome'
        })

        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'id':'senha',
            'placeholder': 'Digite sua senha',
            })
        
        self.fields['email'].widget = forms.EmailInput(attrs={
            'id':'email',
            'placeholder': 'Digite seu email'
        })

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name','email','password1', 'password2')

