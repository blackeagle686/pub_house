from django.db import models
from django.utils.translation import gettext_lazy as _

class Author(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='author_profile')
    name = models.CharField(_("Name"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True, allow_unicode=True)
    biography = models.TextField(_("Biography"), blank=True)
    photo = models.ImageField(
        _("Photo"),
        upload_to="authors/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")
        ordering = ["name"]

    def __str__(self):
        return self.name
