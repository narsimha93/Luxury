from . import views
from django.urls import path

urlpatterns = [
    path("book/",views.booking,name="book"),
    path("booking/",views.allbookings,name="allbookings"),
    #payment apis
    path('payment/<list_id>', views.payment, name = 'payment'),
    path('callback/',views.callback, name='callback')
   # path('handlerequest/', views.handlerequest, name = 'handlerequest'),

]
