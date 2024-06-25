from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from .fields import OrderField
from django.template.loader import render_to_string

class Subject(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering=['title']

class Course(models.Model):

    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_courses')
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='courses')
    students=models.ManyToManyField(User,related_name='courses_joined',blank=True)

    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200,unique=True)

    overview=models.TextField()
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    class Meta:
        ordering=['-created']    

class Module(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='modules')
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])


    def __str__(self):
        return f'{self.order}_{self.title}'
    class Meta:
        ordering=['order']

class Content(models.Model):
    module=models.ForeignKey(Module,on_delete=models.CASCADE,related_name='contents')
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE,limit_choices_to={'model__in':('Text','Image','Video','File')})
    object_id=models.PositiveIntegerField()
    item=GenericForeignKey('content_type','object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering=['order']



class ItemBase(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_related')
    title=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(f'courses/content/{self._meta.model_name}.html',{'item': self})


class Text(ItemBase):
    content=models.TextField()

class Image(ItemBase):
    image=models.ImageField(upload_to='images')

class File(ItemBase):
    file=models.FileField(upload_to='files')

class Video(ItemBase):
    url=models.URLField()
    