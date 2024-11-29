from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.cache import cache  # Import para cache
from .models import Veiculo, Usuario, Aluguel
from .decorators import login_required_custom
from django.contrib import messages
from django.utils import timezone
from PIL import Image
import hashlib
import numpy as np
import os
import random

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def get_usuario(request):
    """Recupera o usuário logado e verifica se é funcionário."""
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        return get_object_or_404(Usuario, id=usuario_id)
    return None

def verificar_funcionario(usuario):
    """Verifica se o usuário é funcionário."""
    return usuario and usuario.categoria == 'funcionario'

def buscar_veiculos(request):
    query = request.GET.get('q', '')
    if query:
        veiculos = Veiculo.objects.filter(marca__icontains=query) | Veiculo.objects.filter(modelo__icontains=query)
        results = [{
            "id": v.id,
            "marca": v.marca,
            "modelo": v.modelo,
            "imagem_url": v.imagem.url if v.imagem else None
        } for v in veiculos[:5]]
        return JsonResponse({"results": results})
    return JsonResponse({"results": []})

def register(request):
    usuario_logado = get_usuario(request)
    
    if verificar_funcionario(usuario_logado) is False:
        messages.error(request, "Você não tem permissão para registrar novos usuários.")
        return redirect('home')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = hash_senha(request.POST.get('senha'))
        email = request.POST.get('email')
        categoria = request.POST.get('categoria', 'visitante' if not usuario_logado else request.POST.get('categoria'))
        foto = request.FILES.get('foto')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Esse email já está em uso.")
            return redirect('register')

        Usuario.objects.create(nome=nome, senha=senha, email=email, categoria=categoria, foto=foto)
        messages.success(request, "Usuário registrado com sucesso.")
        return redirect('login')

    return render(request, 'locadora/register.html', {
        'permitir_escolha_categoria': verificar_funcionario(usuario_logado)
    })

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = hash_senha(request.POST['senha'])

        usuario = Usuario.objects.filter(email=email).first()
        if usuario and usuario.senha == senha:
            request.session['usuario_id'] = usuario.id
            return redirect('home_funcionario' if verificar_funcionario(usuario) else 'veiculos')
        messages.error(request, "Usuário não encontrado ou senha incorreta.")

    return render(request, 'locadora/login.html')

@login_required_custom
def home_funcionario(request):
    usuario = get_usuario(request)
    if not verificar_funcionario(usuario):
        return redirect('home')

    return render(request, 'locadora/home_funcionario.html', {'usuario': usuario})

from django.shortcuts import render
import random

def cor_predominante(image_path):
    # Abre a imagem e converte para RGBA para lidar com transparência
    image = Image.open(image_path).convert("RGBA")
    # Filtra apenas os pixels opacos (ignora os pixels totalmente transparentes)
    pixels = [pixel for pixel in image.getdata() if pixel[3] > 0]

    if not pixels:  # Se não houver pixels opacos, retorne uma cor padrão
        return "rgb(33, 33, 33)"
    
    # Converte os pixels para RGB e calcula a cor predominante
    pixels_rgb = [(r, g, b) for r, g, b, a in pixels]
    predominant_color = max(set(pixels_rgb), key=pixels_rgb.count)
    return f"rgb{predominant_color}"

from django.core.cache import cache
import random
from django.shortcuts import render
from .models import Veiculo

from django.core.cache import cache
import random
from django.shortcuts import render
from .models import Veiculo

def home_visitante(request):
    usuario = get_usuario(request)
    is_funcionario = verificar_funcionario(usuario)

    # Obter o veículo mais recente para exibição principal
    veiculo_recente = Veiculo.objects.order_by('-id').first() if Veiculo.objects.exists() else None
    veiculo_modelo_upper = veiculo_recente.modelo.upper() if veiculo_recente else ""
    cor = "rgb(255, 255, 255)"
    
    if veiculo_recente:
        try:
            cor = cor_predominante(veiculo_recente.imagem.path)
        except ValueError:
            cor = "rgb(33, 33, 33)"

    # Obter veículos que possuem um banner, excluindo o último veículo cadastrado
    veiculos_com_banner = Veiculo.objects.filter(banner__isnull=False).exclude(id=veiculo_recente.id)

    # Garantir que o banner seja escolhido aleatoriamente semanalmente
    banner_veiculo = cache.get('banner_veiculo')
    if not banner_veiculo:
        if veiculos_com_banner.exists():
            # Converte o queryset em lista para permitir a seleção aleatória
            veiculos_com_banner = [veiculo for veiculo in veiculos_com_banner if veiculo.banner]  
            if veiculos_com_banner:
                banner_veiculo = random.choice(veiculos_com_banner)
                cache.set('banner_veiculo', banner_veiculo, timeout=7 * 24 * 60 * 60)  # Cache por uma semana
        else:
            banner_veiculo = None

    # Obtenha a URL do banner, caso o banner esteja definido
    banner_url = banner_veiculo.banner.url if banner_veiculo and banner_veiculo.banner else None

    # Seleciona os 4 veículos mais recentes, excluindo o último
    veiculos_selecionados = Veiculo.objects.all().order_by('-id')[1:5]
    veiculos_selecionados2 = Veiculo.objects.all().order_by('-id')[6:9]

    context = {
        'veiculos': Veiculo.objects.all(),  # Todos os veículos
        'veiculos_selecionados': veiculos_selecionados,  # 4 veículos mais recentes excluindo o último
        'veiculos_selecionados2': veiculos_selecionados2, 
        'veiculo': veiculo_recente,  # Último veículo cadastrado para exibição principal
        'cor': cor,
        'usuario': usuario,
        'is_funcionario': is_funcionario,
        'veiculo_modelo_upper': veiculo_modelo_upper,
        'banner_url': banner_url,  # URL do banner selecionado para a semana
    }
    return render(request, 'locadora/home.html', context)


@login_required_custom
def register_vehicle(request):
    usuario = get_usuario(request)
    if not verificar_funcionario(usuario):
        return redirect('home')

    if request.method == 'POST':
        veiculo = Veiculo(
            placa=request.POST['placa'],
            marca=request.POST['marca'],
            modelo=request.POST['modelo'],
            preco_diaria=request.POST['preco_diaria'],
            descricao=request.POST.get('descricao', ''),
            imagem=request.FILES.get('imagem'),
            imagem2=request.FILES.get('imagem2'),
            banner=request.FILES.get('banner')
        )
        veiculo.save()
        messages.success(request, "Veículo registrado com sucesso.")
        return redirect('veiculos')

    return render(request, 'locadora/register_vehicle.html')

@login_required_custom
def editar_veiculo(request, veiculo_id):
    usuario = get_usuario(request)
    if not verificar_funcionario(usuario):
        return redirect('home')

    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    if request.method == 'POST':
        veiculo.placa = request.POST['placa']
        veiculo.marca = request.POST['marca']
        veiculo.modelo = request.POST['modelo']
        veiculo.preco_diaria = request.POST['preco_diaria']
        veiculo.descricao = request.POST.get('descricao', '')
        if 'imagem' in request.FILES:
            veiculo.imagem = request.FILES['imagem']
        if 'imagem2' in request.FILES:
            veiculo.imagem2 = request.FILES['imagem2']
        if 'banner' in request.FILES:
            veiculo.banner = request.FILES['banner']
        
        veiculo.save()
        messages.success(request, "Veículo atualizado com sucesso.")
        return redirect('veiculos')

    return render(request, 'locadora/editar_veiculo.html', {'veiculo': veiculo})

def veiculos(request):
    usuario = get_usuario(request)
    is_funcionario = verificar_funcionario(usuario)
    
    veiculos = Veiculo.objects.all()
    return render(request, 'locadora/veiculos.html', {'usuario': usuario, 'veiculos': veiculos, 'is_funcionario': is_funcionario})

@login_required_custom
def detalhes_veiculo(request, veiculo_id):
    usuario = get_usuario(request)
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    
    alugado_por_usuario = Aluguel.objects.filter(cliente=usuario, veiculo=veiculo, data_entrega__isnull=True).exists()
    is_funcionario = verificar_funcionario(usuario)

    context = {
        'usuario': usuario,
        'veiculo': veiculo,
        'alugado_por_usuario': alugado_por_usuario,
        'is_funcionario': is_funcionario
    }
    return render(request, 'locadora/detalhes_veiculo.html', context)

@login_required_custom
def devolver_veiculo(request, veiculo_id):
    usuario = get_usuario(request)
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    aluguel = Aluguel.objects.filter(cliente=usuario, veiculo=veiculo, data_entrega__isnull=True).first()

    if aluguel:
        aluguel.data_entrega = timezone.now().date()
        aluguel.save()
        veiculo.disponivel = True
        veiculo.save()
        messages.success(request, "Veículo devolvido com sucesso.")
    else:
        messages.error(request, "Erro ao processar devolução.")

    return redirect('detalhes_veiculo', veiculo_id=veiculo_id)

@login_required_custom
def alugar_veiculo(request, veiculo_id):
    usuario = get_usuario(request)
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)

    if not veiculo.disponivel:
        messages.error(request, "Este veículo está indisponível para aluguel.")
        return redirect('detalhes_veiculo', veiculo_id=veiculo_id)

    if request.method == 'POST':
        data_prevista_entrega = request.POST.get('data_devolucao')
        
        if data_prevista_entrega:
            Aluguel.objects.create(
                cliente=usuario,
                veiculo=veiculo,
                data_aluguel=timezone.now().date(),
                data_prevista_entrega=data_prevista_entrega
            )
            veiculo.disponivel = False
            veiculo.save()
            messages.success(request, "Veículo alugado com sucesso!")
            return redirect('detalhes_veiculo', veiculo_id=veiculo_id)
        else:
            messages.error(request, "Por favor, selecione uma data de devolução.")

    return redirect('detalhes_veiculo', veiculo_id=veiculo_id)

@login_required_custom
def lista_alugueis(request):
    alugueis = Aluguel.objects.all()
    veiculos = Veiculo.objects.all()
    return render(request, 'locadora/lista_alugueis.html', {'alugueis': alugueis, 'veiculos': veiculos})

def cor_predominante(imagem_path):
    if not os.path.exists(imagem_path):
        raise ValueError("Imagem não encontrada.")

    img = Image.open(imagem_path).convert("RGB").resize((100, 100))
    data = np.array(img)

    if data.ndim == 3 and data.shape[2] == 3:
        media_cor = data.mean(axis=(0, 1))
        return f"rgb({int(media_cor[0])}, {int(media_cor[1])}, {int(media_cor[2])})"
    else:
        raise ValueError("Formato de imagem não suportado.")

def logout(request):
    request.session.pop('usuario_id', None)
    messages.success(request, "Você saiu com sucesso.")
    return redirect('home')
