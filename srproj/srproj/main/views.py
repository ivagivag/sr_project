from django.shortcuts import render


def display_main_page(request):
    """
    Different main pages are displayed based on the fact whether the user has been authenticated or not
    """
    if request.user.is_authenticated:
        return render(request, 'base/index_private.html')
    else:
        return render(request, 'base/index_public.html')


def resource_not_found(request, template_name='base/404.html', **kwargs):
    """
    Custom 404 NotFound page
    The status code must be passed on to render, otherwise status code 200 is returned,
    which compromises the Unit tests
    """
    return render(request, template_name, status=404)


def forbidden(request, template_name='base/403.html', **kwargs):
    """
    Custom 403 Forbidden page
    The status code must be passed on to render, otherwise status code 200 is returned,
    which compromises the Unit tests
    """
    return render(request, template_name, status=403)


def data_error(request, template_name='base/500.html', **kwargs):
    """
    Custom 403 Forbidden page
    The status code must be passed on to render, otherwise status code 200 is returned,
    which compromises the Unit tests
    """
    return render(request, template_name, status=500)