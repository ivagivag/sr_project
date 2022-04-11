from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('faq/', TemplateView.as_view(template_name='base/faq_public.html'), name='faq'),
    path('contacts/', TemplateView.as_view(template_name='base/contacts_public.html'), name='contacts'),
]
