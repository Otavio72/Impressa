from django.shortcuts import render, redirect,get_object_or_404
from .forms import UploadForm
from .models import Carrinho, ItemCarrinho, Produto, Pedido, ItemPedido
from .ProcessarArquivo import ProcessarPDF
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from usuarios.models import CustomUser

# Create your views here.

@login_required
def remover_item_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, carrinho__user=request.user)
    item.delete()
    return redirect('index')

@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    user = request.user
    

    # Tenta recuperar o carrinho do usuário com base na sessão
    carrinho_id = request.session.get("carrinho_id")
    
    if carrinho_id:
        carrinho = Carrinho.objects.filter(id=carrinho_id, user=user).first()
    else:
        carrinho = None

    # Se não existir, cria um novo carrinho e salva o ID na sessão
    if not carrinho:
        carrinho = Carrinho.objects.create(user=user)
        request.session["carrinho_id"] = carrinho.id

    itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)


    # Adiciona o produto ao carrinho (usando um modelo intermediário ItemCarrinho, por exemplo)
    item, criado = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho,
        produto=produto,
        defaults={'quantidade': 1}
    )

    if not criado:
        item.quantidade += 1
        item.save()

    return redirect('index')

    
    
@login_required
def modal_carrinho(request):
    #carrinho, created = Carrinho.objects.get_or_create(user=request.user)

    carrinho_id = request.session.get("carrinho_id")
    if not carrinho_id:
        return render(request, 'partials/modal_carrinho.html',{
            'itens_carrinho': [],
            'total': 0,
            'quantidade_carrinho': 0,
        })
    
    carrinho = Carrinho.objects.filter(id=carrinho_id, user=request.user).first()
    if not carrinho:
        return render(request, 'partials/modal_carrinho.html',{
            'itens_carrinho': [],
            'total': 0,
            'quantidade_carrinho': 0,
        })


    itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)
    total = sum(item.total for item in itens_carrinho)
    

    return render(request, 'partials/modal_carrinho.html', {
        'itens_carrinho': itens_carrinho,
        'total': total,
        
    })


def index(request):
    return render(request, 'index.html')

@login_required
def impressao(request):
    form = UploadForm()
    resultado = None
    numero_paginas = None
    preco = None
    nome = None
    url_arquivo = None
    produto = None

    #produtos = Produto.objects.all()
    
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            arquivo = form.cleaned_data['arquivo']


            caminho_arquivo = f'media/temp/{arquivo.name}'

            

            with open(caminho_arquivo, 'wb+') as destino:
                for chunk in arquivo.chunks():
                    destino.write(chunk)

            
            colorido = request.POST.get('colorido') == 'on'
            encadernar = request.POST.get('encadernar') == 'on'
            papel_90g = request.POST.get('papel_90g') == 'on'
            tipo = request.GET.get("tipo") or request.POST.get("tipo") or "jato"

            processar = ProcessarPDF(caminho_arquivo, colorido=colorido, encadernar=encadernar,papel_90g=papel_90g,tipo=tipo)

            if caminho_arquivo.endswith('.pdf'):
                numero_paginas, preco, nome = processar.pdf_preco()


            elif caminho_arquivo.endswith('.png') or caminho_arquivo.endswith('.jpg') or caminho_arquivo.endswith('jpeg'):
                numero_paginas = 1
                nome ,preco = processar.preco()


            produto = Produto.objects.create(
                nome=nome,
                preco=preco,
                tipo=tipo,
                opcoes={
                    "colorido": colorido,
                    "encadernar": encadernar,
                    "papel_90g": papel_90g
                },
                #url_arquivo = f"/media/temp/{arquivo.name}"

            )

        
            resultado = f"Arquivo: {nome}, Páginas: {numero_paginas}, Preço: {preco}"
            url_arquivo = f"/media/temp/{arquivo.name}"

        

    return render(request, 'impressao.html', {
        'resultado': resultado,
        'form':form,
        'url_arquivo': url_arquivo,
        'produto': produto,
        
        })




@login_required
def pagamento(request):

    carrinho_id = request.session.get("carrinho_id")
    if not carrinho_id:
        return render(request, 'partials/modal_carrinho.html',{
            'itens_carrinho': [],
            'total': 0,
            'quantidade_carrinho': 0,
        })
    
    carrinho = Carrinho.objects.filter(id=carrinho_id, user=request.user).first()
    if not carrinho:
        return render(request, 'partials/modal_carrinho.html',{
            'itens_carrinho': [],
            'total': 0,
            'quantidade_carrinho': 0,
        })

    itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)
    quantidade_carrinho = sum(item.quantidade for item in itens_carrinho)
    total = sum(item.total for item in itens_carrinho)

    return render(request, 'pagamento.html' , {
        'itens_carrinho': itens_carrinho,
        'total': total,
        'quantidade_carrinho':quantidade_carrinho,

    })

@login_required
def finalizar_pagamento(request):
    print(">>> FINALIZAR_PAGAMENTO VIEW CHAMADA")

    print(">>> SESSION:", dict(request.session))
    carrinho_id = request.session.get("carrinho_id")
    print(">>> CARRINHO ID:", carrinho_id)

    if not carrinho_id:
        print(">>> carrinho_id não encontrado na sessão")
        return redirect('pagamento')

    carrinho = Carrinho.objects.filter(id=carrinho_id, user=request.user).first()
    print(">>> CARRINHO:", carrinho)

    if not carrinho:
        print(">>> Carrinho não encontrado")
        return redirect('pagamento')

    itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)
    print(">>> ITENS CARRINHO:", list(itens_carrinho))

    if not itens_carrinho.exists():
        print(">>> Nenhum item no carrinho")
        return redirect('pagamento')

    total = sum(item.total for item in itens_carrinho)
    print(">>> TOTAL:", total)

    pedido = Pedido.objects.create(user=request.user, total=total, carrinho=carrinho)
    print(">>> PEDIDO CRIADO:", pedido)

    for item in itens_carrinho:
        item_pedido = ItemPedido.objects.create(
            pedido=pedido,
            produto=item.produto,
            quantidade=item.quantidade,
            preco_unitario=item.produto.preco,
        )
        print(">>> ITEM PEDIDO:", item_pedido)

    #carrinho.delete()
    del request.session["carrinho_id"]

    return redirect('index')



def quemsomos(request):
    return render(request, 'quemsomos.html')



