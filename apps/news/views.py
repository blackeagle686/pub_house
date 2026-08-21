from django.views.generic import ListView, DetailView
from .models import NewsArticle

class NewsListView(ListView):
    model = NewsArticle
    template_name = 'news/news_list.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        return NewsArticle.objects.filter(published=True)

class NewsDetailView(DetailView):
    model = NewsArticle
    template_name = 'news/news_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return NewsArticle.objects.filter(published=True)
