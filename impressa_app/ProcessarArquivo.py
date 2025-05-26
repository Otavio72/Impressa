from PyPDF2 import PdfReader
import os

class ProcessarPDF:
    def __init__(self,diretorio,tipo="jato", colorido=False, encadernar=False, papel_90g=False):
        
        self.tipo = {
        "laser": {"base": 0.30, "colorido": 1.50},
        "jato": {"base": 0.20, "colorido": 0.50},
        "outros": {"base": 0.25, "colorido": 1.00},
}

        tipo_preco = self.tipo.get(tipo, {"base":0.20, "colorido": 0.50})
        self.preco_base = tipo_preco["base"]
        self.preco_colorido = tipo_preco["colorido"]

        #self.preco_base = self.tipo.get(tipo, 0.20)
        #self.preco_colorido = self.tipo.get(tipo,{}).get("colorido", 0.50)

        #self.preco_colorido = None
        self.preco_encadernar = 20
        self.preco_papel90g = 1
        self.pag_numero = 0
        self.colorido = colorido
        self.encadernar = encadernar
        self.papel_90g = papel_90g
        self.caminho_completo = os.path.normpath(diretorio) 
        
        self.pag_preco = 0
        self.preco_unitario = 0

    def pdf_preco(self):
        with open(self.caminho_completo, 'rb') as pdf:
            ler_PDF = PdfReader(pdf)
            self.pag_numero = len(ler_PDF.pages)
            

            if self.colorido:
                self.pag_preco = self.pag_numero * self.preco_colorido
            else:
                self.pag_preco = self.pag_numero * self.preco_base

            if self.encadernar:
                self.pag_preco += self.preco_encadernar
            
            if self.papel_90g:
                self.pag_preco += self.pag_numero * self.preco_papel90g
            
            preco_formatado = f"{self.pag_preco:.2f}"
            pdf_nome = os.path.basename(self.caminho_completo)

        return self.pag_numero, preco_formatado, pdf_nome
    
    def preco(self):
        if self.colorido:
            self.preco_unitario = 1 * self.preco_colorido
        else:
            self.preco_unitario = 1 * self.preco_base

        if self.encadernar:
            self.preco_unitario += self.preco_encadernar
        
        if self.papel_90g:
            self.preco_unitario += 1 * self.preco_papel90g
        
        
    
        preco_formatado = f"{self.preco_unitario:.2f}"
        nome_arquivo = os.path.basename(self.caminho_completo)
        return nome_arquivo, preco_formatado
