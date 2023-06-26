from django.urls import path
from api import views

urlpatterns = [
    path("chat", views.ChatMessageView.as_view(), name="chat"),
    # Add any other API URLs specific to your 'api' app here.
]
