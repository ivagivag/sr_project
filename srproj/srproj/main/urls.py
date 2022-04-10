from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
# from srproj.tickets.views.ticket_views import display_main_page

urlpatterns = [
    # path('', display_main_page, name='main page'),
    path('faq/', TemplateView.as_view(template_name='base/faq_public.html'), name='faq'),
    path('contacts/', TemplateView.as_view(template_name='base/contacts_public.html'), name='contacts'),
]

# handler404 = 'srproj.main.views.resource_not_found'
# handler403 = 'srproj.main.views.forbidden'
