from django.contrib import admin
from .models import Usuario,  Disciplina, Sala, Reserva_ambiente
from django.contrib.auth.admin import UserAdmin
'''
    Configurando página admin 🔐 
    Possibilitando o registro de usuários pela página de admin 
'''
class UsuarioAdmin(UserAdmin):
    list_display = ('ni', 'telefone', 'data_contratacao', 'data_nascimento','tipo')

    fieldsets = UserAdmin.fieldsets + (
        (None,{'fields': ('ni', 'telefone', 'data_contratacao', 'data_nascimento','tipo')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None,{'fields': ('ni', 'telefone', 'data_contratacao', 'data_nascimento','tipo')}),
    )
# Acima passamos os campos que são necessários preencher na pag admin

# Declarando Users
admin.site.register(Usuario,UsuarioAdmin)

# Declarando Disciplinas
admin.site.register(Disciplina)

# Declarando Salas
admin.site.register(Sala)

# Declarando Reserva_ambientes
admin.site.register(Reserva_ambiente)
