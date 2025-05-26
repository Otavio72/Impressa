from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50)
    opcoes = models.JSONField(blank=True, null=True)
    quantidade = models.PositiveIntegerField(default=1)
    url_arquivo = models.URLField()
    
    def __str__(self):
        return self.nome
    
class Carrinho(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carrinho de {self.user.username}'
    
class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    quantidade = models.PositiveIntegerField(default=1)
    tipo = models.CharField(max_length=50)

    @property
    def total(self):
        return self.quantidade * self.produto.preco
    
    def __str__(self):
        return f'{self.produto.nome} x {self.quantidade}'
    
class Pedido(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    data_criado = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=[('Em andamento', 'Em andamento'), ('Concluido', 'Concluido')], default='Em andamento')
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Pedido {self.id} para {self.user.username}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total(self):
        return self.quantidade * self.preco_unitario
    



    


