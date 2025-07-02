from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

# Modelo que representa um produto enviado para impressão
class Produto(models.Model):
    nome = models.CharField(max_length=255) # Nome do arquivo
    preco = models.DecimalField(max_digits=10, decimal_places=2) # Preço calculado
    tipo_impressao = models.CharField(max_length=50) # Tipo de impressora usada (ex: jato, laser)
    opcoes = models.JSONField(blank=True, null=True)# Opções selecionadas (ex: cor, encadernação)
    quantidade = models.PositiveIntegerField(default=1) # Quantidade padrão
    url_arquivo = models.FileField() # Caminho do arquivo enviado
    
    def __str__(self):
        return self.nome

# Carrinho de compras associado a um usuário    
class Carrinho(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Dono do carrinho
    criado_em = models.DateTimeField(auto_now_add=True) # Data de criação do carrinho

    def __str__(self):
        return f'Carrinho de {self.user.username}'

# Representa um item dentro de um carrinho
class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE) # Carrinho ao qual pertence
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE) # Produto relacionado
    nome = models.CharField(max_length=255) # Nome do item
    quantidade = models.PositiveIntegerField(default=1) # Quantidade do item

    @property
    def total(self):
        return self.quantidade * self.produto.preco # Valor total do item no carrinho
    
    def __str__(self):
        return f'{self.produto.nome} x {self.quantidade}'

# Pedido finalizado por um usuário    
class Pedido(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Usuário que fez o pedido
    numero_pedido_usuario = models.PositiveBigIntegerField(editable=False) # Número sequencial para cada usuário
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE) # Carrinho convertido em pedido
    data_criado = models.DateTimeField(auto_now_add=True) # Data de criação
    endereco = models.CharField(max_length=255) # Endereço de envio
    complemento = models.CharField(max_length=255, blank=True, null=True) # Complemento (ex: Casa, Apartamento)
    pagamento = models.CharField(max_length=50) # Método de pagamento
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    status = models.CharField(max_length=255, choices=[('Em andamento', 'Em andamento'), ('Concluido', 'Concluido')], default='Em andamento')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('user', 'numero_pedido_usuario') # Garante que o numero do pedido seja único por usuário
        ordering = ['-data_criado'] # Pedidos mais recentes primeiro
    
    # Gera automaticamente o número sequencial do pedido por usuário
    def save(self, *args, **kwargs):
        if not self.numero_pedido_usuario:
            from django.db.models import Max
            ultimo_numero = Pedido.objects.filter(user=self.user).aggregate(Max('numero_pedido_usuario'))['numero_pedido_usuario__max'] or 0
            self.numero_pedido_usuario = ultimo_numero + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Pedido {self.id} para {self.user.username}'

# Itens individuais dentro de um pedido
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens') # Pedido ao qual pertence
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE) # Produto associado
    quantidade = models.PositiveIntegerField() # Quantidade comprada
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2) # Preço unitário no momento da compra

    @property
    def total(self):
        return self.quantidade * self.preco_unitario # Total deste item no pedido

# Perfil com informações adicionais (ex: usuario, endereco_padrao) 
class Perfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Relacionamento 1-1 com o usuário
    endereco_padrao = models.TextField(blank=True,null=True) # Endereço salvo para facilitar novos pedidos
    



    


