from django.contrib import admin
from .models import Usuario, Veiculo, Aluguel


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'categoria', 'last_login')
    search_fields = ('nome', 'email')
    list_filter = ('categoria',)

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'preco_diaria')
    search_fields = ('placa', 'marca', 'modelo')


@admin.register(Aluguel)
class AluguelAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'veiculo', 'data_aluguel', 'data_prevista_entrega', 'data_entrega')
    search_fields = ('cliente__nome', 'veiculo__placa')
    list_filter = ('data_aluguel', 'data_entrega')

