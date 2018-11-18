"""Comment Model"""
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.conf import settings

from posts.models import Post

# Create your models here.
class Comment(models.Model):
    """comment model"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    # Normal foreignkey that is tied to the post model
    # post = models.ForeignKey(Post)

    # Generic foreignkey needs 3 fields so we can use the module to tie it to another mode
        # content-type can be any model in the project
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
        # object_id has to be passed from the instance
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)

    # def get_absolute_url(self):
    #     return reverse('comments:display', kwargs={'id': self.id})
