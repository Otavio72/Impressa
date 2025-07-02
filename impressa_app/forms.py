from django import forms

# Formulário de upload de arquivos utilizado na página de impressão
class UploadForm(forms.Form):
    # Campo que permite o envio de um arquivo pelo usuário
    arquivo = forms.FileField()



