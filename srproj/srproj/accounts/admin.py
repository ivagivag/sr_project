from django.contrib import admin

from .models import Account, Company, AccountProfile
from django.contrib.auth.admin import UserAdmin


@admin.register(AccountProfile)
class AccountProfileAdmin(admin.ModelAdmin):
    list_display = ('account', 'first_name', 'last_name', 'phone')


class ProfileInline(admin.StackedInline):
    model = AccountProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'account'


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'contract_number', 'valid_to', 'update_time')
    readonly_fields = ('update_time',)


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'last_login', 'is_active', 'is_external', 'is_restricted', 'company')
    readonly_fields = ('last_login', 'password')
    ordering = ('company', '-last_login',)
    inlines = (ProfileInline,)
    list_filter = ('company', 'is_active', 'is_restricted', )
    fieldsets = (
        (None, {
            'fields': ('company', )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_external', 'is_restricted',
            )
        }),
        ('Group Membership', {
            'fields': (
                'groups',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', 'company')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_external', 'is_restricted',
            )
        }),
        ('Group Membership', {
            'fields': (
                'groups',
            )
        }),
    )
