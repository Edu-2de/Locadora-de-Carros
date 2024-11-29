from django.shortcuts import redirect

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        print(f"Session ID: {request.session.get('usuario_id')}") 
        if 'usuario_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper