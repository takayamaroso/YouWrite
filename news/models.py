from django.db import models
from django.utils import timezone
# Create your models here.
#記事のモデル
class Article(models.Model):
    author = models.ForeignKey('auth.User')#外部キー　多対１
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    image = models.ImageField(blank=True, upload_to='images/', default='images/no-image.jpg')

    #記事公開
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

class Comment(models.Model):
    #外部キー　多対１
    article = models.ForeignKey('news.Article', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    #評価値
    evaluation_value = models.IntegerField(help_text='0~5の範囲で入力してください')


    def __str__(self):
        return self.text