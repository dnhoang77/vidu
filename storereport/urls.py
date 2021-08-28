from django.urls import path
from . import views

app_name = 'storereport'
urlpatterns = [
    path('easypdf', views.html_to_pdf, name='pivot_data'),
]