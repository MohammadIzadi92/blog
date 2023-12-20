from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from . import models


# Create your views here.

# def list_blog(request):
#     blogs = models.Article.objects.published()
#     context = {
#         "blogs": blogs
#     }
#     return render(request, "blog/list.html", context)


class ArticleList(ListView):
    # model = models.Article
    queryset = models.Article.objects.published()
    context_object_name = 'blogs'
    template_name = 'blog/list.html'
    # pageinate_by = 4


# def detail_blog(request,slug):
#     blog = get_object_or_404(models.Article.objects.published(),slug=slug)
#     context = {
#         "blog": blog
#     }
#     return render(request, "blog/detail.html", context)


class ArticleDetail(DetailView):
    # model = models.Article
    template_name = 'blog/detail.html'
    context_object_name = 'blog'
    
    def get_object(self, **kwargs):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(models.Article.objects.published(), slug=slug)
        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)
        return article


# def category(request,slug):
#     blogs = get_object_or_404(models.Category,slug=slug,status=True).articles.published()
#     context = {
#         "blogs": blogs
#     }
#     return render(request, "blog/category.html", context)


class CategoryList(ListView):
    context_object_name = 'blogs'
    template_name = 'blog/category.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(models.Category, slug=slug, status=True).articles.published()
        return category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


# def api(request):
#     data = {
#         "1":{"title":"mobile","author":"mohammad","rate":10},
#         "2":{"title":"robot","author":"sahar","rate":20},
#     }
#     return JsonResponse({"new":data})


class SearchList(ListView):
    template_name = 'blog/search.html'

    def get_queryset(self):
        global articles
        search = self.request.GET.get('q')
        articles = models.Article.objects.filter(Q(title__icontains = search) | Q(description__icontains = search))
        return articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = articles
        return context
