import datetime

from . import models
from . import forms
import re
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, F, Value

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# thư viện cho việc sử dụng email
from MyStore.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import feedparser

subcategory_list = models.SubCategory.objects.all()
subcategory = 0
search_str = ''

def index(request):
    tbgd = models.SubCategory.objects.filter(category=1)
    ddnb = models.SubCategory.objects.filter(category=2)
    product_list = models.Product.objects.order_by("-public_day")
    most_viewed_list = models.Product.objects.order_by("-viewed")[:3]
    newest = product_list[0]
    twenty_newest = product_list[:20]

    return render(request, "store/index.html",
                  {'newest': newest,
                   'twenty_newest': twenty_newest,
                   'most_viewed_list': most_viewed_list,
                   'subcategories': subcategory_list,
                   'tbgd': tbgd,
                   'ddnb': ddnb,
                   'subcategory':subcategory,
                   'search_str':search_str
                   })


def shop(request, pk):
    product_list = []
    subcategory_name = ''
    if pk != 0:
        product_list = models.Product.objects.filter(
            subcategory=pk).order_by("-public_day")
        selected_sub = models.SubCategory.objects.get(pk = pk)
        subcategory_name = selected_sub.name
    else:
        product_list = models.Product.objects.order_by("-public_day")

    three_newest = product_list[:3]

    page = request.GET.get('page', 1)  # trang bat dau
    paginator = Paginator(product_list, 9)  # so product/trang

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, "store/shop.html",
                  {'three_newest': three_newest,
                   'subcategories': subcategory_list,
                   'products': products,
                   'pk': pk,
                   'subcategories': subcategory_list,
                   'subcategory_name': subcategory_name,
                   })


def product_detail(request, pk):
    product_select = models.Product.objects.get(pk=pk)
    # khi người dùng chọn xem 1 sản phẩm > tăng view của sản phẩm thêm 1
    models.Product.objects.filter(pk=product_select.pk).update(viewed=F('viewed') + 1)
    product_select.refresh_from_db()
    return render(request, "store/product.html",
                  {'product': product_select,
                   'subcategories': subcategory_list,
                   })


def cart(request):
    return render(request, 'store/cart.html',
                  {'subcategories': subcategory_list,
                   })


def checkout(request):
    return render(request, 'store/checkout.html',
                  {'subcategories': subcategory_list,
                   })


def contact(request):
    return render(request, 'store/contact.html',
                  {'subcategories': subcategory_list, }
                  )

def show_base(request):
    return render(request, 'store/base.html'
                  )

def search_form(request):
    global subcategory
    global search_str
    product_items = 0
    three_newest = models.Product.objects.all().order_by("-public_day")[:3]
    product_list = []
    if request.method == 'GET':
        form = forms.FormSearch(request.GET, models.Product)

        if form.is_valid():
            subcategory = form.cleaned_data['subcategory_id']
            search_str = form.cleaned_data['name']
            if subcategory != 0:
                product_list = models.Product.objects.filter(
                    subcategory=subcategory, name__contains=search_str).order_by("-public_day")
                #select * from product where subcategory = 1 and name like '%tủ%'
            else:
                product_list = models.Product.objects.filter(
                    name__contains=search_str).order_by("-public_day")

        product_items = len(product_list)

        page = request.GET.get('page', 1)
        paginator = Paginator(product_list, 9)  # so product/trang

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render(request, "store/shop.html",
                      {'three_newest': three_newest,
                       'subcategories': subcategory_list,
                       'products': products,
                       'pk': subcategory,
                       'subcategories': subcategory_list,
                       'product_items': product_items,
                       'subcategory': subcategory,
                       'search_str': search_str
                       })

def register(request):
    now = datetime.datetime.now()
    registered = False
    if request.method == "POST":
        form_user = forms.UserForm(data=request.POST)
        form_por = forms.UserProfileInfoForm(data=request.POST)
        if (form_user.is_valid() and form_por.is_valid() and form_user.cleaned_data['password'] == form_user.cleaned_data['confirm']):
            user = form_user.save()
            user.set_password(user.password)
            user.save()

            profile = form_por.save(commit=False)
            profile.user = user
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            profile.save()

            registered = True
        if form_user.cleaned_data['password'] != form_user.cleaned_data['confirm']:
            form_user.add_error('confirm', 'The passwords do not match')
            print(form_user.errors, form_por.errors)
    else:
        form_user = forms.UserForm()
        form_por = forms.UserProfileInfoForm()

    last_visit = request.session.get('last_visit', False)
    username = request.session.get('username',0)
    return render(request, "store/register.html", {'user_form': form_user,
                                                     'profile_form': form_por,
                                                     'registered': registered,
                                                     'last_visit': last_visit,
                                                     'today': now,
                                                     'username': username})

def user_login(request):
    now = datetime.datetime.now()
    last_visit = request.session.get('last_visit', False)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            result = "Hello " + username
            request.session['username'] = username
            username = request.session.get('username', 0)
            return render(request, "store/login.html", {'login_result': result,
                                                          'username': username,
                                                          'today': now,
                                                          'last_visit': last_visit,})
        else:
            print("You can't login.")
            print("Username: {} and password: {}".format(username, password))
            login_result = "Username or password is incorrect!"
            return render(request, "store/login.html", {'login_result': login_result,
                                                          'last_visit': last_visit,
                                                          'today': now,
                                                          'last_visit': last_visit,
                                                          })
    else:
        return render(request, "store/login.html", {'last_visit': last_visit,
                                                  'today': now,
                                                  })


@login_required
def user_logout(request):
    now = datetime.datetime.now()
    last_visit = request.session.get('last_visit', False)
    logout(request)         
    result = "You're logged out. You can login again."
    return render(request, "store/login.html", {'logout_result': result,
                                                  'last_visit': last_visit,
                                                  'today': now,
                                                  })

def subscribe(request):
    now = datetime.datetime.now()
    last_visit = request.session.get('last_visit', False)
    username = request.session.get('username', 0)
    if request.method == 'POST':
        email_address = request.POST.get("email")        
        subject = 'Welcome to Stories for Children website'
        message = 'Hope you are enjoying the stories!'        
        recepient = str(email_address)        

        html_content = '<h2 style="color:blue"><i>Dear Reader,</i></h2>'\
                        + '<p>Welcome to <strong>Stories for Children</strong> website.</p>' \
                        + '<h4 style="color:red">'+ message +'</h4>'      
        
        msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [recepient])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # send_mail(subject, message, EMAIL_HOST_USER,
        #           [recepient], fail_silently=False)        

        result = "Our email was sent to your mail box. Thank you."

        return render(request, 'base.html', { 'today': now,
                                                      'username': username,
                                                      'last_visit': last_visit,
                                                      'result': result,                                                      
                                                      })
    return render(request, 'base.html', {
                                                  'today': now,
                                                  'username': username,
                                                  'last_visit': last_visit,                                                  
                                                  })

def read_feeds(request):
    news_feed = feedparser.parse("http://feeds.feedburner.com/bedtimeshortstories/LYCF")
    
    entry = news_feed.entries
    now = datetime.datetime.now()
    last_visit = request.session.get('last_visit', False)
    username = request.session.get('username', 0)
    return render(request, "store/feeds.html",
                  {'today': now,
                   'last_visit': last_visit,
                   'username': username,
                   'feeds': entry})

def google_map(request):
    return render(request, "store/google_map.html")
