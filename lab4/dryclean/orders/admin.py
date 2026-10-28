from django.contrib import admin
from .models import Branch, Client, Service, Contract, Item


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1


class ContractAdmin(admin.ModelAdmin):
    list_display = ('number', 'client', 'branch', 'receiver', 'get_excerpt',
                    'date_received', 'has_discount', 'total')
    list_filter = ('branch', 'date_received')       
    inlines = [ItemInline]


class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'phone', 'visits', 'is_regular')
    search_fields = ('last_name', 'phone')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'base_price')


admin.site.register(Branch)
admin.site.register(Client, ClientAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Contract, ContractAdmin)
