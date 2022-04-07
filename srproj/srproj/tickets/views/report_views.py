from django.template.loader import get_template
from xhtml2pdf import pisa

from srproj.tickets.models.core_models import TicketEventLog

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def event_log_render_pdf_view(request, tid):
    template_path = 'tickets/report_event_log.html'
    response = HttpResponse(content_type='application/pdf')
    log_events = TicketEventLog.objects.filter(ticket_id=tid)
    context = {
        'log_events': log_events,
        'tid': tid,
    }

    filename = f"event_log_SR_{context['tid']}.pdf"
    response['Content-Disposition'] = f'attachment; filename={filename}'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
