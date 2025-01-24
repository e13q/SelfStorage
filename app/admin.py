from django.contrib import admin
from .models import CustomUser, Client, FAQ, Address, Warehouse, Box, Order,AdvertisingLink
from .advertisement_short_link import shorten_link,count_clicks

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "is_active", "is_staff")
    search_fields = ("email", "username")
    list_filter = ("is_active", "is_staff")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "phone_number")
    search_fields = ("full_name", "phone_number")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category')
    search_fields = ('question', 'answer', 'category')
    list_filter = ('category',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("street_address", "city")
    search_fields = ("street_address", "city")


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("address", "advantage", "temperature", "ceiling")
    search_fields = ("address__street_address", "advantage")


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ("number", "storage", "floor", "length", "width", "height", "price", "is_occupied")
    search_fields = ("number", "storage__address__street_address")
    list_filter = ("is_occupied", "floor")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def status_display(self, obj):
        return obj.get_status_display()

    list_display = ("date", "status_display", "expiration", "box", "client", "address")
    search_fields = ("client__full_name", "box__number", "address")
    list_filter = ("status", "date", "expiration")
    ordering = ("expiration", "status")
    readonly_fields = ('status_display',)

    status_display.short_description = 'Статус'

@admin.register(AdvertisingLink)
class AdvertisingLinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'short_url', 'visits_number')
    ordering = ['visits_number']
    actions = ['count_clicks', 'shorten_link']

    @admin.action(description='Узнать количество переходов')
    def count_clicks(self, requests, queryset):
        for obj in queryset:
            obj.visits_number = count_clicks(obj.short_url)
            obj.save()

    @admin.action(description='Сократить ссылки')
    def shorten_link(self, requests, queryset):
        for obj in queryset:
            obj.short_url = shorten_link(obj.url)
            obj.save()