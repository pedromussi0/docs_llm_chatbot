from django.urls import path
from . import views

urlpatterns = [
    path("submit-message", views.submit_message, name="submit_message"),
]
