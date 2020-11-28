from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('add-news/', views.add_news, name="add_news"),
    path('my-all-news/', views.all_news, name="my_all_news"),
    path('edit/<slug>-<id>/', views.edit_my_news, name="edit_news"),
    path('read/<slug>-<id>/', views.read_full_news, name="full_news"),
    path('delete/<slug>-<id>/', views.deletes, name="delete_news")
]   