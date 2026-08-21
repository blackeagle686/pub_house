from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('search/', views.DashboardGlobalSearchView.as_view(), name='search'),
    path('login/', views.DashboardLoginView.as_view(), name='login'),
    
    # Books
    path('books/', views.DashboardBooksView.as_view(), name='books'),
    path('books/add/', views.DashboardBookCreateView.as_view(), name='book_add'),
    path('books/<int:pk>/edit/', views.DashboardBookUpdateView.as_view(), name='book_edit'),
    path('books/<int:pk>/delete/', views.DashboardBookDeleteView.as_view(), name='book_delete'),
    path('books/<int:pk>/toggle-featured/', views.DashboardBookToggleFeaturedView.as_view(), name='book_toggle_featured'),
    
    # Orders
    path('orders/', views.DashboardOrdersView.as_view(), name='orders'),
    path('orders/<int:pk>/edit/', views.DashboardOrderUpdateView.as_view(), name='order_edit'),
    
    # Users
    path('users/', views.DashboardUsersView.as_view(), name='users'),
    path('users/add/', views.DashboardUserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/edit/', views.DashboardUserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.DashboardUserDeleteView.as_view(), name='user_delete'),
    path('users/<int:pk>/toggle-status/', views.DashboardUserToggleStatusView.as_view(), name='user_toggle_status'),

    # Manuscripts
    path('manuscripts/', views.DashboardManuscriptsView.as_view(), name='manuscripts'),
    path('manuscripts/<int:pk>/edit/', views.DashboardManuscriptUpdateView.as_view(), name='manuscript_edit'),
    path('manuscripts/<int:pk>/delete/', views.DashboardManuscriptDeleteView.as_view(), name='manuscript_delete'),

    # Authors
    path('authors/', views.DashboardAuthorsView.as_view(), name='authors'),
    path('authors/add/', views.DashboardAuthorCreateView.as_view(), name='author_add'),
    path('authors/<int:pk>/edit/', views.DashboardAuthorUpdateView.as_view(), name='author_edit'),
    path('authors/<int:pk>/delete/', views.DashboardAuthorDeleteView.as_view(), name='author_delete'),
    path('authors/<int:pk>/toggle-status/', views.DashboardAuthorToggleStatusView.as_view(), name='author_toggle_status'),

    # Reports
    path('reports/', views.DashboardReportsView.as_view(), name='reports'),
    path('reports/<int:pk>/edit/', views.DashboardReportUpdateView.as_view(), name='report_edit'),
    path('reports/<int:pk>/delete/', views.DashboardReportDeleteView.as_view(), name='report_delete'),
    path('reports/<int:pk>/action/', views.DashboardReportActionView.as_view(), name='report_action'),
]
