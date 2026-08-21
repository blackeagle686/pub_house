from django.db import models
from django.utils.translation import gettext_lazy as _

class ContactMessage(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=30, blank=True)
    subject = models.CharField(_("Subject"), max_length=255)
    message = models.TextField(_("Message"))
    is_read = models.BooleanField(_("Is Read"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} - {self.name}"

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class Report(models.Model):
    REASON_CHOICES = [
        ('spam', 'محتوى مزعج / سبام'),
        ('inappropriate', 'محتوى غير لائق أو مسيء'),
        ('copyright', 'انتهاك حقوق الملكية'),
        ('other', 'سبب آخر'),
    ]
    STATUS_CHOICES = [
        ('pending', 'قيد المراجعة'),
        ('resolved', 'تم الحل'),
        ('dismissed', 'مرفوض'),
    ]
    
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports', verbose_name=_("Reporter"))
    reason = models.CharField(_("Reason"), max_length=20, choices=REASON_CHOICES)
    description = models.TextField(_("Description"), blank=True)
    
    # Generic Relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    resolved_at = models.DateTimeField(_("Resolved at"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        ordering = ['-created_at']

    def __str__(self):
        return f"بلاغ من {self.reporter.username} - {self.get_status_display()}"
