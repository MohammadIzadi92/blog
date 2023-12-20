from django.contrib.auth import views
from django.urls import path
from .views import (
    ArticleListView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
    Profile,
    Login,
)

app_name = "account"

urlpatterns = [
    path("", ArticleListView.as_view(), name="home"),
    path('login/', Login.as_view(), name='login'),
    path("create/", ArticleCreateView.as_view(), name="article_create"),
    path("update/<int:pk>", ArticleUpdateView.as_view(), name="article_update"),
    path("delete/<int:pk>", ArticleDeleteView.as_view(), name="article_delete"),
    path("profile/", Profile.as_view(), name="profile"),
]
 