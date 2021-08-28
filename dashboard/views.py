from django.http.response import JsonResponse
from django.shortcuts import render
from store import models
from django.core import serializers
# Create your views here.
def dashboard_with_pivot(request):
    return render(request,'dashboard/dashboard_with_pivot.html')

def pivot_data(request):
    dataset = models.Product.objects.all()
    data = serializers.serialize('json',dataset)
    return JsonResponse(data,safe = False)