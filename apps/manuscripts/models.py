from django.db import models

class Manuscript(models.Model):
    STATUS_CHOICES = (
        ('pending', 'قيد المراجعة'),
        ('accepted', 'مقبول'),
        ('rejected', 'مرفوض'),
    )
    
    author_name = models.CharField(max_length=150, verbose_name="اسم المؤلف")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    phone_number = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    title = models.CharField(max_length=200, verbose_name="عنوان العمل")
    idea = models.TextField(verbose_name="فكرة العمل أو ملخصه")
    cover = models.ImageField(upload_to='manuscripts/covers/', null=True, blank=True, verbose_name="تصور مبدئي للغلاف (اختياري)")
    file = models.FileField(upload_to='manuscripts/files/', null=True, blank=True, verbose_name="ملف المخطوطة (PDF/Word)")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="الحالة")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.author_name}"
