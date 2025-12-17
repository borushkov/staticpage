from django.urls import path
from .views import PostList, PostDetail, SearchList, NewsCreate, NewsUpdate, NewsDelete, ArticleCreate, ArticleUpdate, ArticleDelete

urlpatterns = [
   path('', PostList.as_view(), name = 'post_list'), 
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   #Общие
   path('search/', SearchList.as_view(), name='search'),
   #Новости
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    # Статьи
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]