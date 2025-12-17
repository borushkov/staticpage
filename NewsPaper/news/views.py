
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post
from .filters import PostFilter
from .forms import PostForm, NewsForm, ArticleForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 2

class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        # Создаем объект фильтра и сохраняем его в self.filterset
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        # Возвращаем отфильтрованный queryset
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['filterset'] = self.filterset

        context['filter_form'] = self.filterset.form
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

'''class NewsList(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(POST_TYPES='Новость', is_published=True)
    
class ArticleList(ListView):
    model = Post
    template_name = 'article_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(POST_TYPES='Статья', is_published=True)
'''

class NewsCreate( CreateView):
    model = Post
    form_class = NewsForm
    template_name = 'create_news.html'
    success_url = reverse_lazy('posts.html')

class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = "edit_news.html"

class NewsDelete(DeleteView):
    model = Post
    template_name = 'delete_news.html'
    success_url = reverse_lazy('posts.html')

class ArticleCreate(CreateView):
    model = Post
    form_class = ArticleForm
    template_name = 'create_article.html'
    success_url = reverse_lazy('posts.html')

class ArticleUpdate(UpdateView):
    form_class = ArticleForm
    model = Post
    template_name = "edit_article.html"

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'delete_article.html'
    success_url = reverse_lazy('posts.html')

class ProtectedView(TemplateView):
    template_name = 'protected_page.html'
    




