from django.apps import AppConfig

# Configuração da aplicação 'impressa_app'
class ImpressaAppConfig(AppConfig):
    # Define o nome do app e o tipo padrão de campo automático para as models
    default_auto_field = 'django.db.models.BigAutoField'

    # Nome da aplicação que será usado pelo Django
    name = 'impressa_app'
