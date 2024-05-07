from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . models import Vendor, PurchaseOrder, HistoricalPerformance
from . serializers import VendorSerializer, PurchaseOrderSerializer
from . utils import update_on_time_delivery_rate, update_quality_rating_avg, update_average_response_time, update_fulfillment_rate

def main(request):
    return HttpResponse("Hello world!")


class VendorDetails(APIView):
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #validated_data = serializer.validated_data
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        queryset = Vendor.objects.all()
        serializer =VendorSerializer(queryset, many=True)
        return Response(serializer.data)



@api_view(['GET', 'PUT', 'DELETE'])
def vendordetails(request, pk):
    try:
        vendor_instance = Vendor.objects.get(id=pk)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        vedor_serializer = VendorSerializer(vendor_instance)
        return Response(vedor_serializer.data)

    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vendor_instance.delete()
        return Response({"message": "Vendor deleted successfully."}, status=status.HTTP_204_NO_CONTENT)




class PurchaseOrderDeatils(APIView):

    def post(self, request):
        serializer=PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        vendor_id = request.query_params.get('vendor')
        if vendor_id is not None:
            queryset = PurchaseOrder.objects.filter(vendor=vendor_id)
            serializer = PurchaseOrderSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            queryset = PurchaseOrder.objects.all()
            seralizer = PurchaseOrderSerializer(queryset, many=True)
            return Response(seralizer.data, status=status.HTTP_200_OK)
    



@api_view(['GET', 'PUT', 'DELETE'])
def purchaseOrderDeatils(request, pk):
    try:
        purchase_instance = PurchaseOrder.objects.get(id=pk)
    except PurchaseOrder.DoesNotExist:
        return Response({"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(purchase_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PurchaseOrderSerializer(purchase_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        purchase_instance.delete()
        return Response({"message": "Purchase Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    



@api_view(['GET'])
def vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    historical_performance = HistoricalPerformance.objects.create(
        vendor=vendor,
        date=timezone.now(),  
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate,
    )

    update_on_time_delivery_rate(vendor)
    update_quality_rating_avg(vendor)
    update_average_response_time(vendor)
    update_fulfillment_rate(vendor)

   
    serializer = VendorSerializer(vendor)
    performance_data = {
        "on_time_delivery_rate": vendor.on_time_delivery_rate,
        "quality_rating_avg": vendor.quality_rating_avg,
        "average_response_time": vendor.average_response_time,
        "fulfillment_rate": vendor.fulfillment_rate,
    }

    return Response(performance_data, status=status.HTTP_200_OK)



@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    try:
        po = PurchaseOrder.objects.get(id=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response({"message": "Purchase Order not found."}, status=status.HTTP_404_NOT_FOUND)

    po.acknowledgment_date = timezone.now()
    po.save()

    
    update_average_response_time(po.vendor)

    return Response({"message": "Purchase Order acknowledged successfully."}, status=status.HTTP_200_OK)
