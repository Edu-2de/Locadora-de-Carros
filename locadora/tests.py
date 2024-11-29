from django.test import TestCase
from .models import Usuario

class UsuarioModelTest(TestCase):
    def setUp(self):
        
        self.usuario = Usuario.objects.create(
            nome="Teste Usuario",
            email="teste@exemplo.com",
            senha="senha123", 
            categoria="funcionario"
        )

    def test_usuario_creation(self):
        
        self.assertEqual(self.usuario.nome, "Teste Usuario")
        self.assertEqual(self.usuario.email, "teste@exemplo.com")
        self.assertEqual(self.usuario.categoria, "funcionario")

    def test_usuario_str(self):
     
        self.assertEqual(str(self.usuario), "Teste Usuario teste@exemplo.com - funcionario")

    def test_usuario_unique_email(self):
       
        with self.assertRaises(Exception):
            Usuario.objects.create(
                nome="Outro Usuario",
                email="teste@exemplo.com",
                senha="senha456",
                categoria="visitante"
            )
