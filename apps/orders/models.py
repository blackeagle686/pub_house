from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from apps.books.models import Book

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', _('قيد المراجعة')),
        ('approved', _('مقبول')),
        ('shipped', _('مشحون')),
        ('delivered', _('تم التسليم')),
        ('cancelled', _('ملغي')),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name=_('User'))
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(_('Total Price'), max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    FORMAT_CHOICES = (
        ('paperback', _('ورقي')),
        ('ebook', _('إلكتروني')),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_format = models.CharField(_('Format'), max_length=20, choices=FORMAT_CHOICES)
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    price = models.DecimalField(_('Price at time of purchase'), max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} ({self.get_book_format_display()})"
