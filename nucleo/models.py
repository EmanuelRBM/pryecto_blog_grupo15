from django.db import models

from django.conf import settings

from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.deletion import PROTECT





class Tag(models.Model):
  name = models.CharField(max_length=40)

  def __str__(self):
      return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    category = models.ForeignKey(Category, on_delete=PROTECT, default=1)
    title = models.CharField(max_length=200, db_index=True)

    slug = models.SlugField(max_length=200, db_index=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    #content = models.TextField()
    content = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=options, default='draft')
    image = models.ImageField(upload_to='', blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)

    

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title



    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)
    


# comentarios

class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.name)

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)



