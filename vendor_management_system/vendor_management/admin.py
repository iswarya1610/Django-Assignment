from django.contrib import admin
from .models import Vendor, PurchaseOrder, HistoricalPerformance

# Register your models here.


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_details', 'address', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
    search_fields = ['name']

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'vendor', 'order_date', 'delivery_date', 'quantity', 'status']
    search_fields = ['po_number']
    list_filter = ['status', 'delivery_date']
    date_hierarchy = 'order_date'

@admin.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
    search_fields = ['vendor__name']
    date_hierarchy = 'date'