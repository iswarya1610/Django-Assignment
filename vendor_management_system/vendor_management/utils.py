from django.utils import timezone
from . models import Vendor, PurchaseOrder
from django.db.models import Count, Avg

def update_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now())
    
    if completed_pos.count() > 0:
        on_time_delivery_rate = (on_time_deliveries.count() / completed_pos.count()) * 100
    else:
        on_time_delivery_rate = 0.0

    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.save()

def update_quality_rating_avg(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    
    if completed_pos.count() > 0:
        quality_rating_avg = completed_pos.aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0.0
    else:
        quality_rating_avg = 0.0

    vendor.quality_rating_avg = quality_rating_avg
    vendor.save()

def update_average_response_time(vendor):
    acknowledged_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)

    if acknowledged_pos.exists():
        response_times = [
            (po.acknowledgment_date - po.issue_date).total_seconds()
            for po in acknowledged_pos
            if po.acknowledgment_date is not None  
        ]

        if response_times:  
            avg_response_time = sum(response_times) / len(response_times)
        else:
            avg_response_time = 0.0
    else:
        avg_response_time = 0.0

    vendor.average_response_time = avg_response_time
    vendor.save()

def update_fulfillment_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    successful_fulfillments = completed_pos.exclude(issue_date__isnull=True)
    
    if completed_pos.count() > 0:
        fulfillment_rate = (successful_fulfillments.count() / completed_pos.count()) * 100
    else:
        fulfillment_rate = 0.0

    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()