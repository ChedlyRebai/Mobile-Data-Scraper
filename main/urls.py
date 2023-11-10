from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
   # path("process_form",views.process_form,name="process_form"),
   # path("chekform",views.chekform,name="chekform"),
  #  path("/check/", views.checkboxes, name="checkboxes"),
    path('my-url/', views.my_view, name='my_view'),
]
