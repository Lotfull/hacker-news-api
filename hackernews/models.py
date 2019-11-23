from django.db import models


class Post(models.Model):
    title = models.TextField()
    url = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

    @staticmethod
    def create(title, url):
        post, created = Post.objects.get_or_create(
            title=title,
            url=url
        )
        if created:
            post.save()

        return post
