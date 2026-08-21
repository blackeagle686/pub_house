from django.urls import path
from . import views

app_name = 'manuscripts'
urlpatterns = [
    path('submit/', views.SubmitManuscriptView.as_view(), name='submit'),
    path('success/', views.SubmitSuccessView.as_view(), name='submit_success'),
]
