from django.urls import path
from . import views
from .views import ArticleUpdateView, ArticleDeleteView
from accounts.views import register_view, login_view, logout_view, profile_view

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.get_article_by_category, name='get_article_by_category'),
    path('tag/<int:tag_id>/', views.get_article_by_tag, name='get_article_by_tag'),
    path('article/<int:article_id>', views.detail_article, name="article_detail"),
    path('add_article/', views.add_article, name="add_article"),
    path('add_category/', views.add_category, name="add_category"),
    path('add_tag/', views.add_tag, name="add_tag"),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('', views.index, name="home"),
    path('profile/<int:pk>', profile_view, name="profile"),
    path('add_comment/<int:article_id>/', views.add_comment, name='add_comment'),
    path('update/<int:pk>/', ArticleUpdateView, name="news_update"),
    path('delete/<int:pk>/', ArticleDeleteView, name="news_delete"),
    path('like_article/<int:article_id>/', views.like_article, name='like_article'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name="delete_comment"),
]
