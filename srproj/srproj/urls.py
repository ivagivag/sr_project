from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from srproj.main.views import display_main_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('srproj.accounts.urls')),
    path('ticket/', include('srproj.tickets.urls')),
    path('report/', include('srproj.reports.urls')),
    path('misc/', include('srproj.miscellaneous.urls')),
    path('index/', include('srproj.main.urls')),
    path('', display_main_page, name='main page'),
    # path('faq/', TemplateView.as_view(template_name='base/faq_public.html'), name='faq'),
    # path('contacts/', TemplateView.as_view(template_name='base/contacts_public.html'), name='contacts'),
]

handler404 = 'srproj.main.views.resource_not_found'
handler403 = 'srproj.main.views.forbidden'
handler500 = 'srproj.main.views.data_error'
