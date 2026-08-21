from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.authors.models import Author

class Category(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, allow_unicode=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True, allow_unicode=True)
    
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books",
        verbose_name=_("Author")
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
        verbose_name=_("Category")
    )

    description = models.TextField(_("Description"))
    
    cover = models.ImageField(
        _("Cover"),
        upload_to="books/"
    )
    
    isbn = models.CharField(
        _("ISBN"),
        max_length=20,
        blank=True
    )
    
    publication_year = models.PositiveIntegerField(
        _("Publication Year"),
        null=True,
        blank=True
    )
    
    pages = models.PositiveIntegerField(
        _("Pages"),
        null=True,
        blank=True
    )
    
    language = models.CharField(
        _("Language"),
        max_length=50,
        default="العربية"
    )
    
    # E-commerce & Publishing Fields
    paperback_price = models.DecimalField(_("Paperback Price"), max_digits=8, decimal_places=2, null=True, blank=True)
    ebook_price = models.DecimalField(_("E-Book Price"), max_digits=8, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(_("Stock Quantity"), default=0)
    is_published = models.BooleanField(_("Is Published"), default=False)
    
    # Homepage Featured
    is_featured = models.BooleanField(_("Is Featured on Homepage"), default=False)
    featured_order = models.PositiveIntegerField(_("Featured Order"), default=0)
    
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        avg = self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0.0

    @property
    def review_count(self):
        return self.reviews.count()

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name=_("Book"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', verbose_name=_("User"))
    rating = models.PositiveIntegerField(
        _("Rating"), 
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(_("Comment"), blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ['-created_at']
        unique_together = ('book', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}/5)"
