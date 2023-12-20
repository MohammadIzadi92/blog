from django import template
from ..models import Category , Article
from django.db.models import Count , Q , Avg
from datetime import datetime , timedelta
from django.contrib.contenttypes.models import ContentType
from star_ratings.models import Rating

register = template.Library()


@register.simple_tag
def title():
    return "سایت من"


@register.inclusion_tag('partials/_header.html')
def category_tags():
    category = Category.objects.filter(status=True)
    context = {
        "category": category
    }
    return context

@register.inclusion_tag('partials/_sidebar.html')
def popular_articles_tags():
    last_month = datetime.today() - timedelta(days=30)
    popular_articles = Article.objects.published().annotate(
        count = Count('hits',filter=Q(articlehit__created__gt = last_month))).order_by('-count','-publish')[:5] 
    context = {
        'articles': popular_articles,
        'title': 'مقالات پر بازدید ماه'
    }
    return context

@register.inclusion_tag('partials/_sidebar.html')
def hot_articles_tags():
    last_month = datetime.today() - timedelta(days=30)
    content_type_id = ContentType.objects.get(app_label='blog', model='article').id
    popular_articles = Article.objects.published().annotate(
        count = Count(
            'comments',
            filter=Q(comments__posted__gt = last_month) and Q(comments__content_type_id = content_type_id))
        ).order_by('-count','-publish')[:5] 
    context = {
        'articles': popular_articles,
        'title': 'مقالات داغ ماه'
    }
    return context

@register.inclusion_tag('partials/_sidebar.html')
def most_rating_articles_tags():
    popular_articles = Article.objects.all().order_by('-ratings__average')[:5] 
    context = {
        'articles': popular_articles,
        'title': 'مقالات محبوب ماه'
    }
    return context