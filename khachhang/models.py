from django.db import models

# Create your models here.
class KhachHang(models.Model):    
    ho_ten = models.CharField(max_length = 264, blank = False)
    ten_dang_nhap=models.CharField(max_length = 50, blank = False)
    mat_khau=models.CharField(max_length = 50, blank = False)
    phone = models.CharField(max_length = 20)
    email = models.EmailField(blank = False)  
    dia_chi = models.TextField()

    def __str__(self):
        return self.ho_ten
    
    class Meta:
        db_table=u'KhachHang'
