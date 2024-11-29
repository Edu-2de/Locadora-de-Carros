from .models import Usuario
from .views import hash_senha  

class UsuarioBackend:
    def authenticate(self, request, email=None, senha=None, **kwargs):
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.senha == hash_senha(senha):  
                return usuario
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
