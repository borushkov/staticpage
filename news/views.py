
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category, User
from .filters import PostFilter
from .forms import PostForm, NewsForm, ArticleForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from .models import Category
from django.views import View
import os
from django.conf import settings
from .tasks import hello 
from django.http import HttpResponse

class PostList(ListView):
    model = Post
    template_name = 'news/posts_p.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 6

    

class SearchList(ListView):
    model = Post
    template_name = 'news/search_p.html'
    context_object_name = 'search'
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
    template_name = 'news/post_detail.html'
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
    template_name = 'news/form.html'
    success_url = reverse_lazy('post_list')

class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = "news/form.html"

class NewsDelete(DeleteView):
    model = Post
    template_name = 'news/delete.html'
    success_url = reverse_lazy('post_list')

class ArticleCreate(CreateView):
    model = Post
    form_class = ArticleForm
    template_name = 'news/form.html'
    success_url = reverse_lazy('post_list')

class ArticleUpdate(UpdateView):
    form_class = ArticleForm
    model = Post
    template_name ='news/form.html'

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news/delete.html'
    success_url = reverse_lazy('post_list')

class ProtectedView(TemplateView):
    template_name = 'protected_page.html'


class Email(View):
    def post(self, request, *args, **kwargs):
        mail = Category(
            name = request.POST['name'], 
            subscribers = request.POST['subscribers']
        )
        mail.save()

        send_mail(
            subject  = None,
            message = 'emails/new_post.html',
            from_email= os.getenv("EMAIL_NAME"),
            recipient_list = [mail.subscribers]
        )
class IndexView(View):
    def get(self, request):
        hello.delay()
        return HttpResponse("Hello, Its Celery")


