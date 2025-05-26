from django.shortcuts import render, redirect
from .forms import CustomCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from impressa_app.models import Carrinho, ItemCarrinho, Pedido
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def perfil(request):
    pedidos = Pedido.objects.filter(user=request.user).order_by('-data_criado')

    return render(request, 'perfil.html', {
        'pedidos': pedidos,
    })
 


def register(request):
    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    else:
        form = CustomCreationForm()
    return render(request, 'register.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha invalidos')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')