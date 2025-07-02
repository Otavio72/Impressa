"""
URL configuration for impressa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from impressa_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

# Define as rotas para as paginas principais
urlpatterns = [
    path('admin/', admin.site.urls), # Painel administrativo do Django
    path('', views.index, name='index'), # Pagina principal
    path('usuarios/', include('usuarios.urls')), # Rotas relacionadas a usuários (login, cadastro, perfil)
    path('pagamento/', views.pagamento, name='pagamento'), # Pagina de pagamento
    path('quemsomos/', views.quemsomos, name='quemsomos'), # Pagina "Quem somos"
    path('finalizar_pagamento/', views.finalizar_pagamento, name='finalizar_pagamento'), # Finalização de compra
    path('modal_carrinho/', views.modal_carrinho, name='modal_carrinho'), # Modal do Carrinho (carregado via AJAX)
    path('remover-item/<int:item_id>/', views.remover_item_carrinho, name='remover_item_carrinho'), # Remove item do carrinho
    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'), # Adiciona item ao carrinho
    path('impressao/', views.impressao, name='impressao'), # Página de envio de arquivos para impressão
]

# Servir arquivos estáticos e de mídia no modo DEBUG (durante o desenvolvimento)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
