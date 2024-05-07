from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('api/vendors/', views.VendorDetails.as_view()),
    path('api/vendors/<int:pk>/', views.vendordetails, name='vendordetails'),
    path('api/purchase_orders/', views.PurchaseOrderDeatils.as_view()),
    path('api/purchase_orders/<int:pk>/', views.purchaseOrderDeatils, name='purchaseOrderDeatils'),

    path('api/vendors/<int:vendor_id>/performance/', views.vendor_performance, name='vendor_performance'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order, name='acknowledge_purchase_order'),
]