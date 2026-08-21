from django.views.generic import ListView, DetailView
from .models import Author

class AuthorListView(ListView):
    model = Author
    template_name = 'authors/author_list.html'
    context_object_name = 'authors'
    paginate_by = 12

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'authors/author_detail.html'
    context_object_name = 'author'
    
    def get_queryset(self):
        return Author.objects.prefetch_related('books__category')
