from django.urls import path
from . import views

app_name = 'khachhang'
urlpatterns = [
    path('tao', views.index, name='index'),
    path('doc', views.read_cookie, name='doc'),
    path('del', views.del_cookie, name='del'),
]