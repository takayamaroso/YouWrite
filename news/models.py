from django.db import models
from django.utils import timezone
# Create your models here.
class Article(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def comments(self):
        return self.comments#.filter(approved_comment=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey('news.Article', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    evaluation_value = models.IntegerField()


    def __str__(self):
        return self.text