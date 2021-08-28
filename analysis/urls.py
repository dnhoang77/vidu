from django.urls import path
from . import views

app_name = 'analysis'
urlpatterns = [
    path('series', views.work_with_series, name='series.html'),
    
]