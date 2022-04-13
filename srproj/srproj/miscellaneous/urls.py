from django.urls import path, re_path
from srproj.miscellaneous.views.company_views import CompanyCreateView, CompanyModifyView, CompanyListView, \
    CompanyDisplayView, CompanyActDeactView

urlpatterns = [
    path('company/create/', CompanyCreateView.as_view(), name='create company'),
    path('company/modify/<int:pk>', CompanyModifyView.as_view(), name='modify company'),
    path('company/display/<int:pk>', CompanyDisplayView.as_view(), name='display company'),
    path('company/<str:action>/<int:pk>/', CompanyActDeactView.as_view(), name='act deact company'),
    path('company/list/', CompanyListView.as_view(), name='list companies'),

]
