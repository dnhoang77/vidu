from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import pdfkit
from datetime import date
from pdfkit.api import configuration
from store import models
from django.db.models import Count
from django.template.loader import render_to_string
import os

def html_to_pdf(request):
    path_wkhthtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhthtmltopdf)
    today = date.today()
    d = today.strftime("%d/%m/%Y")
    product_list = models.Product.objects.values('subcategory',"subcategory__name").annotate(total = Count('subcategory')).order_by('subcategory')
    html_string=render_to_string('storereport/easyreport.html',{'products':product_list,'day':d})
    pdfkit.from_string(html_string,os.path.join(os.path.expanduser('~'),'Documents','report.pdf'), configuration=config)
    html='<html><body></body><h3>Thong ke da luu vao tep report.pdf</h3></html>'
    return HttpResponse(html)
