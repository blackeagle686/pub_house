from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.books.models import Book
from apps.news.models import NewsArticle
from apps.authors.models import Author
from .models import ContactMessage
from .forms import ContactForm

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 10 featured books ordered by featured_order and then newest
        context['featured_books'] = Book.objects.filter(is_featured=True).select_related('author', 'category').order_by('featured_order', '-id')[:10]
        # 4 latest authors
        context['featured_authors'] = Author.objects.all().order_by('-id')[:4]
        # 3 latest news
        context['latest_news'] = NewsArticle.objects.filter(published=True).order_by('-id')[:3]
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'

class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = 'core/contact.html'
    success_url = reverse_lazy('core:contact')

    def form_valid(self, form):
        messages.success(self.request, "تم إرسال رسالتك بنجاح.")
        return super().form_valid(form)

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .models import Report

@login_required
def submit_report(request):
    if request.method == 'POST':
        model_name = request.POST.get('model_name')  # e.g., 'books.book'
        object_id = request.POST.get('object_id')
        reason = request.POST.get('reason')
        description = request.POST.get('description', '')
        next_url = request.POST.get('next', '/')

        if not all([model_name, object_id, reason]):
            messages.error(request, "بيانات البلاغ غير مكتملة.")
            return redirect(next_url)

        try:
            app_label, model = model_name.split('.')
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            obj = content_type.get_object_for_this_type(id=object_id)
            
            Report.objects.create(
                reporter=request.user,
                reason=reason,
                description=description,
                content_type=content_type,
                object_id=object_id
            )
            messages.success(request, "تم إرسال البلاغ للإدارة لمراجعته. شكراً لك.")
        except (ValueError, ContentType.DoesNotExist, Exception):
            messages.error(request, "حدث خطأ أثناء تقديم البلاغ.")

        return redirect(next_url)
    return redirect('/')
