from django.db import models


class ChatMessage(models.Model):
    sender = models.CharField(
        max_length=100,
        choices=(
            ("user", "User"),
            ("ai", "AI"),
        ),
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
