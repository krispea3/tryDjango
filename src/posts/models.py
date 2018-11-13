""" Future import """
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Post(models.Model):
    """ Post class """
    # Needs to be assigned in VSC as the linter will throw error that objects not defined
    # in Views queryset = Model.object.whatever
    # objects = models.Manager()

    title = models.CharField(max_length=120)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


    def __str__(self):
        return self.title

    # defines the URL of the unique data row
    def get_absolute_url(self):
        """ returning path of unique row """
        # posts:detail the posts is defined in the project urls.py as namespace
        # this allows us to use the same view name for different namespaces
        return reverse("posts:detail", kwargs={'post_id': self.id})
        # %s means string substitution. is defined after the string with %()
        # return "/posts/%s/" %(self.id)

    # Model metadata is “anything that’s not a field”, such as ordering options (ordering),
    # database table name (db_table), or human-readable singular and plural names
    # (verbose_name and verbose_name_plural).
    # None are required, and adding class Meta to a model is completely optional.
    # Here the ordering of a simple fetch will return the rows sorted with most recent timestamp
    # without havin to order it
    class Meta:
        ordering = ["-timestamp", "-updated"]
