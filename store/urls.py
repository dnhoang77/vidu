from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.index, name='index.html'),
    path('shop.html/<int:pk>/', views.shop, name='shop.html'),
    path('search.html', views.search_form, name='search.html'),
    path('product.html/<int:pk>/', views.product_detail, name='product.html'),
    path('cart.html', views.cart, name='cart.html'),
    path('checkout.html', views.checkout, name='checkout.html'),
    path('contact.html', views.contact, name='contact.html'),
    path('base.html', views.show_base, name='base.html'),
    path('register.html', views.register, name='register.html'),
    path('login.html', views.user_login, name='login.html'),
    path('logout.html', views.user_logout, name='logout.html'),
    path('subscribe.html', views.subscribe, name='subscribe.html'),
    path('feeds.html', views.read_feeds, name='feeds.html'),
    path('google_map.html', views.google_map, name='google_map.html'),
]