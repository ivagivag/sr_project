from django.urls import path

from srproj.tickets.views.assessment_views import AssessmentCreateView
from srproj.tickets.views.report_views import event_log_render_pdf_view
from srproj.tickets.views.ticket_views import TicketCreateView, TicketModifyView, \
    TicketAssignView, TicketDeleteView, TicketCloseView, TicketActiveView, display_main_page, \
    TicketResolvedView, TicketDisplayView
from srproj.tickets.views.entry_views import EntryCreateView
from srproj.tickets.views.event_log_view import TicketEventLogView

urlpatterns = [
    path('index/', display_main_page, name='main page'),
    path('active', TicketActiveView.as_view(), name='active tickets'),
    path('resolved', TicketResolvedView.as_view(), name='resolved tickets'),
    path('create/', TicketCreateView.as_view(), name='create ticket'),
    path('modify/<int:pk>/', TicketModifyView.as_view(), name='modify ticket'),
    path('assign/<int:pk>/', TicketAssignView.as_view(), name='assign ticket'),
    path('delete/<int:pk>/', TicketDeleteView.as_view(), name='delete ticket'),
    path('close/<int:pk>/', TicketCloseView.as_view(), name='close ticket'),
    path('display/<int:pk>/', TicketDisplayView.as_view(), name='ticket details'),
    path('entry/create/<int:tid>/', EntryCreateView.as_view(), name='create entry'),
    path('assess/<int:tid>/', AssessmentCreateView.as_view(), name='assess ticket'),
    path('log/<int:tid>/', TicketEventLogView.as_view(), name='event log'),
    path('logpdf/<int:tid>/', event_log_render_pdf_view, name='report event log'),
]

import srproj.tickets.signals