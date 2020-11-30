from django.urls import path
from .api import (add_like, remove_like, add_dislike, remove_dislike, add_comment, get_comment, add_reply, edit_reply, delete_reply)


urlpatterns = [
    path('add-like/', add_like, name="add_like"),
    path('remove-like/', remove_like, name="remove_like"),
    path('add-dislike/', add_dislike, name="add_dislike"),
    path('remove-dislike/', remove_dislike, name="remove_dislike"),
    path('add-comment/', add_comment, name="addComment"),
    path('all_comment/', get_comment, name="getAllComment"),
    path('add-reply/', add_reply, name="add_reply"),
    path('edit-reply/', edit_reply, name="edit_reply"),
    path('delete-reply/<id>/', delete_reply, name="delete_reply"),


]