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
![Modelo Conceitual](https://github.com/acenelio/assets/raw/main/sds1/modelo-conceitual.png)

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

```bash
# clonar repositório
git clone https://github.com/Otavio72/Impressa

Ative o ambiente virtual:
No Windows (PowerShell):
  ```powershell
  .venv\Scripts\Activate.ps1

No Linux/macOS:
source .venv/bin/activate

python manage.py runserver

Acesse o projeto no navegador:
http://127.0.0.1:8000/
```

# Autor
Otávio Ribeiro
www.linkedin.com/in/otávio-ribeiro-57a359197
