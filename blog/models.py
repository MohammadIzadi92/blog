from ipaddress import ip_address
from venv import create
from django.db import models
from django.utils import timezone
from extensions.utils import jalali_convertor
from django.utils.html import format_html
from account.models import User
from django.urls import reverse
# comment
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
# rating
from star_ratings.models import Rating


# Create your models here.
# managers
class ArticlesManager(models.Manager):
    def published(self):
        return self.filter(status="p")


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


# models
class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آی پی')


class Category(models.Model):
    parent = models.ForeignKey("self", default=None, blank=True, null=True, on_delete=models.CASCADE,
                               related_name="children")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    position = models.IntegerField()

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title

    objects = CategoryManager()


class Article(models.Model):
    STATUS_CHOICES = (
        ("d", "پیش نویس"),
        ("p", "منتشر شده"),
        ("i", "در حال بررسی"),
        ("b", "برگشت داده شده"),
    )
    author = models.ForeignKey(User, null=True, related_name='articles', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ManyToManyField(Category, related_name='articles')
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="image")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False, verbose_name="مقاله ویژه")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IPAddress, through='ArticleHit', blank=True, related_name='hits', verbose_name='بازدید ها')
    ratings = GenericRelation(Rating) 

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('account:home')

    def jpublish(self):
        return jalali_convertor(self.publish)

    def category_publish(self):
        return self.category.filter(status=True)

    def thumbnail_tag(self):
        return format_html("<img width=100 hight=75 src='{}'>".format(self.thumbnail.url))

    def category_to_str(self):
        return ' / '.join([category.title for category in self.category_publish()])

    category_to_str.short_description = "دسته یندی ها"
    thumbnail_tag.short_description = "عکس"
    jpublish.short_description = "زمان انتشار"

    objects = ArticlesManager()
    

class ArticleHit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    
    
    
    
    
    
    
    
    
