from django.db import models

class URLMapping(models.Model):
    short_key = models.CharField(max_length=10, unique=True)
    original_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_key} -> {self.original_url}"
