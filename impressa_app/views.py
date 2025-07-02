from django.shortcuts import render, redirect,get_object_or_404
from .forms import UploadForm
from .models import Carrinho, ItemCarrinho, Produto, Pedido, ItemPedido, Perfil
from .ProcessarArquivo import ProcessarPDF
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from PyPDF2.errors import PdfReadError

# Create your views here.

# Remove um item específico do carrinho do usuário logado e redireciona para a página inicial
@login_required
def remover_item_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id, carrinho__user=request.user)
    item.delete()
    return redirect('index')

# Adiciona o produto ao carrinho do usuário logado e redireciona para a página inicial.
# Se o usuário ainda não possuir um carrinho, um novo é criado e salvo na sessão.
# Se o item selecionado já estiver no carrinho, sua quantidade é incrementada.
@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    user = request.user
    
    carrinho_id = request.session.get("carrinho_id")
    
    if carrinho_id:
        carrinho = Carrinho.objects.filter(id=carrinho_id, user=user).first()
    else:
        carrinho = None

    if not carrinho:
        carrinho = Carrinho.objects.create(user=user)
        request.session["carrinho_id"] = carrinho.id



    item, foi_criado = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho,
        produto=produto,
        defaults={'quantidade': 1}
    )

    if not foi_criado:
        item.quantidade += 1
        item.save()

    return redirect('index')

    
# Renderiza o modal do carrinho com os itens do carrinho do usuário logado.
# Se o usuário não possuir um carrinho, um carrinho vazio é renderizado.
@login_required
def modal_carrinho(request):

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

# Renderiza a página inicial do site
def index(request):
    return render(request, 'index.html')

# View responsavel por processar a pagina de impressão.
# Exibe o formulario de upload.
# Valida e salva temporariamento o arquivo recebido
# Processa o arquivo para calcular o preço de impressao com base nas opcoes escolhidas
# Cria um objeto Produto no banco de dados com as informações do arquivo processado
# Retorna os dados para a pagina impressao.html
@login_required
def impressao(request):
    form = UploadForm()
    resultado = None
    numero_paginas = None
    preco = None
    nome = None
    url_arquivo = None
    produto = None
    tipo_impressao = None
    usar_encadernacao = None
    usar_papel_90g = None
    impressao_colorida = None

    # Verifica se é uma requisição POST
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            arquivo = form.cleaned_data['arquivo']

            # Valida extensão do arquivo
            if not arquivo.name.endswith(('.pdf', '.png', '.jpg', '.jpeg')):
                messages.error(request, "Por favor selecione apenas arquivos .pdf, .png, .jpg ou .jpeg")
                return redirect('impressao')

            # Salva o arquivo na pasta temporária
            caminho_arquivo = f'media/temp/{arquivo.name}'
            with open(caminho_arquivo, 'wb+') as destino:
                for chunk in arquivo.chunks():
                    destino.write(chunk)

            # Lê as opções de impressão do fomulário recebido
            impressao_colorida = request.POST.get('impressao_colorida') == 'on'
            usar_encadernacao = request.POST.get('usar_encadernacao') == 'on'
            usar_papel_90g = request.POST.get('usar_papel_90g') == 'on'
            tipo_impressao = request.GET.get("tipo_impressao") or request.POST.get("tipo_impressao") or "jato"

            try:
                # Processa o arquivo
                processador_pdf = ProcessarPDF(caminho_arquivo, impressao_colorida=impressao_colorida, usar_encadernacao=usar_encadernacao, usar_papel_90g=usar_papel_90g, tipo_impressao=tipo_impressao)

                if caminho_arquivo.endswith('.pdf'):
                    numero_paginas, preco, nome = processador_pdf.pdf_preco()
                else:  
                    numero_paginas = 1
                    nome, preco = processador_pdf.png_jpg_preco()

                # Cria o produto no banco com os dados ja processados
                produto = Produto.objects.create(
                    nome=nome,
                    preco=preco,
                    tipo_impressao=tipo_impressao,
                    opcoes={
                        "impressao_colorida": impressao_colorida,
                        "usar_encadernacao": usar_encadernacao,
                        "usar_papel_90g": usar_papel_90g
                    },
                )

                # Define o caminho para a exibição
                url_arquivo = f"/media/temp/{arquivo.name}"

            # Tratamento do erros
            except PdfReadError:
                messages.error(request, "Erro ao ler o PDF")
                return redirect('impressao')

            except FileNotFoundError:
                messages.error(request, "Arquivo não encontrado")
                return redirect('impressao')

            except Exception as e:
                messages.error(request, f"Ocorreu um erro inesperado: {e}")
                return redirect('impressao')

    # Renderiza a página passando os dados ou formulario vazio
    return render(request, 'impressao.html', {
        'form': form,
        'url_arquivo': url_arquivo,
        'produto': produto,
        'preco': preco,
        'nome': nome,
        'numero_paginas': numero_paginas,
        'tipo_impressao': tipo_impressao,
        'impressao_colorida': impressao_colorida,
        'usar_papel_90g': usar_papel_90g,
        'usar_encadernacao': usar_encadernacao,
    })




# View responsável por exivir a página de pagamento
# Recupera o carrinho do usuário logado a partir da sessão
# Soma os valores a e quantidade total dos itens no carrinho
# Renderiza a página de pagamento com essas informações
@login_required
def pagamento(request):

    # Recupera o ID do carrinho salvo na sessão do usuário
    carrinho_id = request.session.get("carrinho_id")

    # Se não ouver carrinho, retorna um carrinho vazio
    if not carrinho_id:
        return render(request, 'partials/modal_carrinho.html',{
            'itens_carrinho': [],
            'total': 0,
            'quantidade_carrinho': 0,
        })
    
    # Busca o carrinho no banco de dados para o usuário
    carrinho = Carrinho.objects.filter(id=carrinho_id, user=request.user).first()
    
    # Se o carrinho não for encontrado (ID inválido ou não pertence ao usuário)
    if not carrinho:
        return render(request, 'partials/modal_carrinho.html',{
            'itens_carrinho': [],
            'total': 0,
            'quantidade_carrinho': 0,
        })

    # Recupera os itens do carrinho
    itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)
    
    # Calcula a quantidade total de itens e o valor total
    quantidade_carrinho = sum(item.quantidade for item in itens_carrinho)
    total = sum(item.total for item in itens_carrinho)

    # Renderiza a página de pagamento com os dados do carrinho
    return render(request, 'pagamento.html' , {
        'itens_carrinho': itens_carrinho,
        'total': total,
        'quantidade_carrinho':quantidade_carrinho,

    })


@login_required
def finalizar_pagamento(request):
    if request.method == "POST":
        carrinho_id = request.session.get("carrinho_id")

        if not carrinho_id:
                return redirect('pagamento')

        carrinho = Carrinho.objects.filter(id=carrinho_id, user=request.user).first()
        
        if not carrinho:
            return redirect('pagamento')

        itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)

        if not itens_carrinho.exists():
            return redirect('pagamento')

        total = sum(item.total for item in itens_carrinho)
            
        endereco = request.POST.get('address')
        complemento = request.POST.get('address2')
    
        estado = request.POST.get('state')

        pagamento = request.POST.get('paymentMethod')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')

        cc_nome = request.POST.get('cc_nome')
        cc_numero = request.POST.get('cc_numero')
        cc_validade = request.POST.get('cc_validade')
        cc_cvv = request.POST.get('cc_cvv')

        billing_address = request.POST.get('same-address')

        if request.POST.get('same-address') == "on":
            shipping_address = billing_address
        
        if request.POST.get('save-info') == "on":
            perfil, created = Perfil.objects.get_or_create(usuario=request.user)
            perfil.endereco_padrao = request.POST.get('save-info')
            perfil.save()

        if not all([cc_nome,cc_numero,cc_validade,cc_cvv]):
            return redirect('pagamento')

        pedido = Pedido.objects.create(
                user=request.user, 
                total=total,
                carrinho=carrinho,
                endereco=endereco,
                complemento = complemento,
                bairro = bairro,
                cidade = cidade,
                estado = estado,
                pagamento = pagamento,
                )
            

        for item in itens_carrinho:
                item_pedido = ItemPedido.objects.create(
                pedido=pedido,
                produto=item.produto,
                quantidade=item.quantidade,
                preco_unitario=item.produto.preco,
                )
                

        
        del request.session["carrinho_id"]

        messages.success(request, "Pedido finalizado com sucesso!")
        return redirect('index')
    
    return redirect('pagamento')



def quemsomos(request):
    return render(request, 'quemsomos.html')



