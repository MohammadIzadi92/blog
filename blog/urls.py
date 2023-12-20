from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # path("",views.list_blog,name="blogs"),
    path("", views.ArticleList.as_view(), name="blogs"), 
    # path("blog/<slug:slug>",views.detail_blog,name="detail_blog"),
    path("blog/<slug:slug>", views.ArticleDetail.as_view(), name="detail_blog"),
    # path("category/<slug:slug>",views.category,name="category"),
    path("category/<slug:slug>", views.CategoryList.as_view(), name="category"),
    # path("api/",views.api,name="api"),
    path("search/", views.SearchList.as_view(), name="search"),
]
