from django.urls import path

from srproj.reports.views import TicketViolatedSla, TicketAssessmentFiltered

urlpatterns = [
    path('feedback/<str:fb>/', TicketAssessmentFiltered.as_view(), name='feedback'),
    path('sla/', TicketViolatedSla.as_view(), name='violated sla'),
]