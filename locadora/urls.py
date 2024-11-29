from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_visitante, name='home'),
    path('funcionarios/', views.home_funcionario, name='home_funcionario'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('veiculos/', views.veiculos, name='veiculos'),
    path('veiculo/<int:veiculo_id>/', views.detalhes_veiculo, name='detalhes_veiculo'),
    path('register_vehicle/', views.register_vehicle, name='register_vehicle'),
    path('editar_veiculo/<int:veiculo_id>/', views.editar_veiculo, name='editar_veiculo'),
    path('alugueis/', views.lista_alugueis, name='lista_alugueis'),
    path('logout/', views.logout, name='logout'),
    path('alugar/<int:veiculo_id>/', views.alugar_veiculo, name='alugar_veiculo'),
    path('veiculo/<int:veiculo_id>/devolver/', views.devolver_veiculo, name='devolver_veiculo'),
    path('veiculos/<int:veiculo_id>/editar/', views.editar_veiculo, name='editar_veiculo'),
    path('buscar_veiculos/', views.buscar_veiculos, name='buscar_veiculos'),

]
