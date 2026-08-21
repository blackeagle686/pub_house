from django.db import models
from django.utils.translation import gettext_lazy as _

class NewsArticle(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True, allow_unicode=True)
    content = models.TextField(_("Content"))
    
    image = models.ImageField(
        _("Image"),
        upload_to="news/",
        blank=True,
        null=True
    )
    
    published = models.BooleanField(_("Published"), default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("News Article")
        verbose_name_plural = _("News Articles")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
