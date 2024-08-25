from django.http import HttpResponseForbidden

def keycloak_role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=role).exists():
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()
        return _wrapped_view
    return decorator

# example usage:

# @keycloak_role_required('agl-intern')
# def some_protected_view(request):
#     # Your view logic here
#     return render(request, 'protected_page.html')
