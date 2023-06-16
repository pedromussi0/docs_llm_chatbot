from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.ChatMessageView.as_view(), name="chat"),
]
