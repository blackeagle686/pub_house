from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Book, Category

class CategoryListView(ListView):
    model = Category
    template_name = 'books/category_list.html'
    context_object_name = 'categories'

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        qs = Book.objects.select_related('author', 'category')
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        return qs

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        return Book.objects.select_related('author', 'category')

class BookSearchView(ListView):
    model = Book
    template_name = 'books/book_search.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Book.objects.select_related('author', 'category').filter(
                Q(title__icontains=query) |
                Q(author__name__icontains=query) |
                Q(category__name__icontains=query)
            )
        return Book.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review

@login_required
def submit_review(request, slug):
    if request.method == 'POST':
        book = get_object_or_404(Book, slug=slug)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
                
            review, created = Review.objects.update_or_create(
                book=book, user=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
            
            if created:
                messages.success(request, "تم إضافة تقييمك بنجاح!")
            else:
                messages.success(request, "تم تحديث تقييمك بنجاح!")
                
        except (ValueError, TypeError):
            messages.error(request, "تقييم غير صالح. الرجاء اختيار تقييم من 1 إلى 5.")
            
        return redirect('books:detail', slug=slug)
    return redirect('books:list')
