from django.contrib.auth.models import User
from django.db import models

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article", blank=True, null=True)
    title = models.CharField(max_length=70)
    image = models.ImageField(null=True, blank=True, upload_to="home/image")
    text = models.TextField()
    status = models.BooleanField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.text[:50]
