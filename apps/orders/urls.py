from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:book_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<str:book_key>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.order_success, name='order_success'),
]
