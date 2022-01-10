from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=False, blank=False)
    slug = models.SlugField(default='', null=True, blank=True)
    intro = models.CharField(default='', max_length=250, null=False, blank=False)
    body = models.TextField(default="", null=False, blank=False)
    image = models.ImageField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp']


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             related_name='comments',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000, null=False, blank=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment on {self.post.title} by {self.user}"

    class Meta:
        ordering = ['timestamp']