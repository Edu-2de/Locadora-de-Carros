from django.shortcuts import redirect
from django.urls import reverse

class CheckUserLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que exigem login
        protected_urls = ['/funcionarios/', '/veiculos/', '/register_vehicle/', '/editar_veiculo/']
        if any(request.path.startswith(url) for url in protected_urls) and 'usuario_id' not in request.session:
            return redirect(reverse('login')) 

        response = self.get_response(request)
        return response