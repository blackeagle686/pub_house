from django.urls import path
from . import views

app_name = 'books'
urlpatterns = [
    path('', views.BookListView.as_view(), name='list'),
    path('search/', views.BookSearchView.as_view(), name='search'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('category/<slug:category_slug>/', views.BookListView.as_view(), name='category_list'),
    path('<slug:slug>/review/', views.submit_review, name='submit_review'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='detail'),
]
