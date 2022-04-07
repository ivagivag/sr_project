from django.contrib import admin

from srproj.tickets.models.base_models import TicketSla
from srproj.tickets.models.core_models import Ticket, TicketWorkFlow, TicketEventLog, TicketAssessment
from srproj.tickets.models.suppl_models import ProductFamily, Product


@admin.register(ProductFamily)
class ProductFamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'domain')
    ordering = ('domain', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'family', 'features', 'version', 'stability', 'date_of_release', 'end_of_support', 'is_active',
    )
    fieldsets = (
        ("Basic", {
            'fields': ('name', 'family', 'features', 'version',)
        }),
        ("Validity", {
            'fields': ('date_of_release', 'end_of_support', 'is_active',)
        }),
    )
    add_fieldsets = (
        ("Basic", {
            'fields': ('name', 'family', 'features', 'version',)
        }),
        ("Validity", {
            'fields': ('date_of_release', 'end_of_support', 'is_active',)
        }),
    )
    ordering = ('family', 'name', 'version', 'is_active')


@admin.register(TicketSla)
class TicketSlaAdmin(admin.ModelAdmin):
    list_display = ('severity', 'reaction_hours', 'remark')
    ordering = ('reaction_hours',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'summary', 'description', 'product', 'creator', 'assignee', 'modifier', 'severity',
        'state', 'register_date', 'resolve_date', 'resolve_due_date', 'rating', 'is_active',
    )
    readonly_fields = (
        'summary', 'description', 'product', 'creator', 'assignee', 'modifier', 'severity',
        'state', 'register_date', 'resolve_date', 'resolve_due_date', 'rating', 'is_active',
    )
    fieldsets = (
        ('Basic', {
            'fields': ('summary', 'description', 'product',)
        }),
        ('Status', {
            'fields': ('severity', 'state', 'rating', 'is_active',)
        }),
        ('People', {
            'fields': ('creator', 'assignee', 'modifier',)
        }),
        ('Dates', {
             'fields': ('register_date', 'resolve_date', 'resolve_due_date',)
        }),
    )
    list_filter = ('state', 'severity', 'product')
    search_fields = ('summary', 'description')


@admin.register(TicketWorkFlow)
class TicketWorkFlowAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'note', 'typ', 'event_time', 'creator')
    readonly_fields = ('ticket', 'note', 'typ', 'event_time', 'creator')
    list_filter = ('typ',)
    search_fields = ('note',)


@admin.register(TicketAssessment)
class TicketAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        'ticket', 'creator', 'event_time', )
    readonly_fields = (
        'ticket', 'reaction', 'reaction_remark', 'resolve', 'resolve_remark',
        'overall', 'overall_remark', 'creator', 'event_time',
    )
    fieldsets = (
        ('Assessments', {
             'fields': ('reaction', 'resolve','overall',),
        }),
        ('Customer Notes', {
            'fields': ('reaction_remark', 'resolve_remark','overall_remark',),
        }),
        ('Customer', {
            'fields': ('creator', 'event_time',),
        }),
    )
    ordering = ('ticket', '-event_time',)


@admin.register(TicketEventLog)
class TicketEventLogAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'event', 'creator', 'event_time')
    readonly_fields = ('ticket', 'event', 'creator', 'event_time')
    search_fields = ('event', )