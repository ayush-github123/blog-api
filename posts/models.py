from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    # image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = GenericRelation('LikeDislike', related_query_name='post_likes')

    def __str__(self):
        return f"{self.title} by {self.user.username}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = GenericRelation('LikeDislike', related_query_name='comment_likes')

    def __str__(self):
        return f"{self.content} by {self.user.username} on Post {self.post}"



class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Model type
    object_id = models.PositiveIntegerField()  # Object ID
    content_object = GenericForeignKey('content_type', 'object_id')  # Dynamic relation

    value = models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])
    created_at = models.DateTimeField(auto_now_add=True)



    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f"{self.user.username} - {'Like' if self.value == 1 else 'Dislike'} on {self.content_type} {self.object_id}"


