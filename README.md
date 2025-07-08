# Impressa 
[![NPM](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Otavio72/Impressa/blob/main/LICENSE) 


# Sobre o projeto
Após utilizarmos um serviço de impressões, minha família e eu identificamos a viabilidade de criarmos nossa própria gráfica. Para isso, decidi desenvolver uma aplicação web completa para facilitar orçamentos e pedidos.

Impressa é uma aplicação web full stack que permite aos usuários enviar documentos nos formatos PDF, PNG e JPEG, gerando orçamentos automáticos baseados na quantidade de páginas e nas configurações selecionadas.

A aplicação também oferece:

Histórico de pedidos

Carrinho de compras e sistema de checkout simulado

Sistema de login e registro de usuários

## Layout web
![Pagina Inicial](https://github.com/Otavio72/assets/blob/main/impressa1.png) ![Orçamento](https://github.com/Otavio72/assets/blob/main/impressa4.png)

![Sobre o projeto](https://github.com/Otavio72/assets/blob/main/impressa5.png)

![Modo escuro](https://github.com/Otavio72/assets/blob/main/impressaescuro.png)

## Modelo conceitual
![Modelo Conceitual](https://github.com/Otavio72/assets/blob/main/modelo_impressa.png)

# Tecnologias utilizadas

## Back end
- Django
- Python

## Front end
- HTML / CSS / JS 
- Bootstrap 5
  
# Como executar o projeto

## Back end
Pré-requisitos: 
Django 5.2
asgiref 3.8.1
sqlparse 0.5.3
tzdata 2025.2
PyPDF2 3.0.1

```bash
# clonar repositório
git clone https://github.com/Otavio72/Impressa

Ative o ambiente virtual:
  python -m venv .venv

No Windows (PowerShell):
  ```powershell
  .venv\Scripts\Activate.ps1

No Linux/macOS:
  source .venv/bin/activate

Instale as dependências:
  pip install -r requirements.txt

Rode as migrações do banco de dados
  python manage.py migrate

python manage.py runserver

Acesse o projeto no navegador:
http://127.0.0.1:8000/
```

👤 Como acessar o sistema
Para acessar o Impressa, faça seu cadastro:
1. Acesse: http://127.0.0.1:8000/usuarios/register/
2. Preencha o formulário de cadastro
3. Após o registro, você será redirecionado para a página inicial

# Autor
Otávio Ribeiro
www.linkedin.com/in/otávio-ribeiro-57a359197
