from django.shortcuts import render
from datetime import datetime
from .models import * 
from django.shortcuts import redirect
from . import forms
from django.contrib.auth.hashers import PBKDF2PasswordHasher

# Create your views here.
def index(request):
    response = render(request, "khachhang/index.html")
    date1 = datetime.now()    
    response.set_cookie('last_visit', date1.strftime('%d-%m-%Y %H:%M:%S'))    
    return response
def read_cookie(request):     
    value = request.COOKIES.get('last_visit')
    text = "<h2>The last time I come here is  %s</h1>" % value
    return render(request, "khachhang/read.html",{'noidung':text})
def del_cookie(request):     
    response = render(request, "khachhang/del.html")
    response.delete_cookie("last_visit")
    return response

def dang_nhap(request):     
    err = ''
    if request.method == "POST": 
        ten=request.POST.get("ten_dang_nhap")
        _mat_khau=request.POST.get("mat_khau")
        ###################################################
        hasher = PBKDF2PasswordHasher()
        encoded = hasher.encode(_mat_khau,'123')

        kh = KhachHang.objects.filter(ten_dang_nhap=ten, mat_khau=encoded)
        if kh.count()>0:
            #print(kh.count())
            #print(kh[0].ho_ten)
            request.session['username'] = kh[0].ho_ten

            return redirect('quan_tri')
        else:
            err='Dang nhap khong thanh cong'
    return render(request, "khachhang/dang_nhap.html",{'err':err})
def quan_tri(request):
    if request.session.has_key('username'):
        username = request.session['username']
        return render(request, 'khachhang/quan_tri.html', {"username" : username})
    else:
        return redirect('dang_nhap')

def dang_xuat(request):
    try:
        if request.session.has_key('username'):
            del request.session['username']
    except:
        pass
    return redirect('dang_nhap')

def dang_ky(request):
    registered = False
    if request.method == "POST":
        form_user = forms.FormDangKy(request.POST, KhachHang)
        #############################
        hasher = PBKDF2PasswordHasher()
        # them validation cho from
        if form_user.is_valid() and form_user.cleaned_data['mat_khau'] == form_user.cleaned_data['confirm']:
            request.POST._mutable = True               
            post = form_user.save(commit = False)            
            post.ho_ten = form_user.cleaned_data['ho_ten']
            post.ten_dang_nhap = form_user.cleaned_data['ten_dang_nhap']
            #############################
            post.mat_khau = hasher.encode(form_user.cleaned_data['mat_khau'],'123')
            post.email = form_user.cleaned_data['email']
            post.phone = form_user.cleaned_data['phone']
            post.email = form_user.cleaned_data['email']
            post.dia_chi = form_user.cleaned_data['dia_chi']
            post.save()
            print("Đã ghi user vào CSDL")            
        elif form_user.cleaned_data['mat_khau'] != form_user.cleaned_data['confirm']:
            form_user.add_error('confirm', 'The passwords do not match')
            print("Password and confirm password are not the same!")

    else:
        form_user = forms.FormDangKy()
    return render(request, "khachhang/registration.html", {'user_form':form_user,'registered': registered})