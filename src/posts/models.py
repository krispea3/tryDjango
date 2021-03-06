""" Future import """
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe 
from markdown_deux import markdown

# With Manager class we can override or create new queryset calls.
# Example Post.objects.all() could be overwritten here by defining function with name 'all'
# Here we create a new one called 'active' so we can now use Post.objects.active() to return
# a queryset with the filters defined here
class PostManager(models.Manager):
    """Model manager"""
    def active(self, *args, **kwargs):
        """Returns only active posts"""
        return super(PostManager, self).filter(draft=False, publish__lte=timezone.now())

def upload_location(instance, filename):
    """set upload location to post_id/filename"""
    return "%s/%s" %(instance.id, filename)
# Create your models here.

class Post(models.Model):
    """ Post class """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    content = models.TextField()
    slug = models.SlugField(unique=True)

    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # Instanciate changed model manager PostManager
    objects = PostManager()

    def __str__(self):
        return self.title

    # defines the URL of the unique data row
    def get_absolute_url(self):
        """ returning path of unique row """
        # posts:detail the posts is defined in the project urls.py as namespace
        # this allows us to use the same view name for different namespaces
        return reverse("posts:detail", kwargs={'post_slug': self.slug})
        # %s means string substitution. is defined after the string with %()
        # return "/posts/%s/" %(self.id)

    # Model metadata is “anything that’s not a field”, such as ordering options (ordering),
    # database table name (db_table), or human-readable singular and plural names
    # (verbose_name and verbose_name_plural).
    # None are required, and adding class Meta to a model is completely optional.
    # Here the ordering of a simple fetch will return the rows sorted with most recent timestamp
    # without havin to order it

    """Return the content as markdown"""
    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    class Meta:
        ordering = ["-timestamp", "-updated"]

def create_slug(instance, new_slug=None):
    """slugify title"""
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = '%s-%s' %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    """create slug when not already"""
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)
