from PyPDF2 import PdfReader
import os

# Classe responsável por processar arquivos enviados e calcular o preço da impressão
class ProcessarPDF:
    def __init__(self,diretorio,tipo_impressao="jato", impressao_colorida=False, usar_encadernacao=False, usar_papel_90g=False):
        
        # Define os preços base para cada tipo de impressão
        self.tabela_precos = {
        "laser": {"base": 0.20, "impressao_colorida": 1.00},
        "jato": {"base": 0.10, "impressao_colorida": 0.30},
        "outros": {"base": 0.15, "impressao_colorida": 0.70},
}
        
        # Seleciona o conjunto de preços com base no tipo de impressão escolhido
        tipo_preco = self.tabela_precos.get(tipo_impressao, {"base":0.15, "impressao_colorida": 0.50})
        self.preco_base = tipo_preco["base"]
        self.preco_colorido = tipo_preco["impressao_colorida"]

        # Define os preços fixos adicionais
        self.preco_encadernar = 15
        self.preco_papel90g = 0.25

        # Armazena os dados recebidos
        self.numero_paginas = 0
        self.impressao_colorida = impressao_colorida
        self.usar_encadernacao = usar_encadernacao
        self.usar_papel_90g = usar_papel_90g
        self.caminho_completo = os.path.normpath(diretorio) 
        
        # Inicializa os valores de preço final
        self.preco_total = 0
        self.preco_unitario = 0

    # Processa arquivos PDF: conta páginas e calcula o preço final 
    def pdf_preco(self):
        # Conta o número de páginas do PDF
        with open(self.caminho_completo, 'rb') as pdf:
            leitor_pdf = PdfReader(pdf)
            self.numero_paginas = len(leitor_pdf.pages)
            
        # Calcula o preço com base nas opções selecionadas
            if self.impressao_colorida:
                self.preco_total = self.numero_paginas * self.preco_colorido
            else:
                self.preco_total = self.numero_paginas * self.preco_base

            if self.usar_encadernacao:
                self.preco_total += self.preco_encadernar
            
            if self.usar_papel_90g:
                self.preco_total += self.numero_paginas * self.preco_papel90g
            
            preco_formatado = f"{self.preco_total:.2f}"
            nome_arquivo_pdf = os.path.basename(self.caminho_completo)

        # Retorna os dados para exibição na view
        return self.numero_paginas, preco_formatado, nome_arquivo_pdf
    
    # Processa arquivos de imagem (.png, .jpg, etc.) e calcula o preço final
    def png_jpg_preco(self):

        # Calcula o preço com base nas opções selecionadas
        if self.impressao_colorida:
            self.preco_unitario = 1 * self.preco_colorido
        else:
            self.preco_unitario = 1 * self.preco_base

        if self.usar_encadernacao:
            self.preco_unitario += self.preco_encadernar
        
        if self.usar_papel_90g:
            self.preco_unitario += 1 * self.preco_papel90g
    
        preco_formatado = f"{self.preco_unitario:.2f}"
        nome_arquivo = os.path.basename(self.caminho_completo)

        # Retorna os dados para exibição na view
        return nome_arquivo, preco_formatado
