from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    senha = models.CharField(max_length=128)  
    email = models.EmailField(max_length=255, unique=True)
    categoria = models.CharField(choices=[('visitante', 'Visitante'), ('funcionario', 'Funcionário')], max_length=50)
    foto = models.ImageField(upload_to='usuarios/', blank=True, null=True)  

    def __str__(self):
        return self.nome

    def set_senha(self, raw_password):
        
        self.senha = make_password(raw_password)
    
    def check_senha(self, raw_password):
        
        return check_password(raw_password, self.senha)


class Veiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    preco_diaria = models.DecimalField(max_digits=8, decimal_places=2)
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='veiculos/', blank=True, null=True)
    imagem2 = models.ImageField(upload_to='veiculos/', blank=True, null=True)
    banner = models.ImageField(upload_to='veiculos/', blank=True, null=True)
    disponivel = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.placa}"

class Aluguel(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data_aluguel = models.DateField()
    data_prevista_entrega = models.DateField()
    data_entrega = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.veiculo} alugado por {self.cliente} em {self.data_aluguel}"

    def duracao_aluguel(self):
        if not self.data_aluguel:
            return 0
        data_final = self.data_entrega or self.data_prevista_entrega
        return (data_final - self.data_aluguel).days
