from django.urls import path

from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('trans/', views.trans, name='trans'),
    path('reviews/',views.postComment,name="reviews")
]