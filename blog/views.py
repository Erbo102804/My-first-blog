from typing import Any, Dict
from django.urls import path  # Добавьте эту строку
from django.utils import timezone
from .models import Post, Category
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
    form = PostForm(request.POST, instance=post)
    form = PostForm(instance=post)

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'news/create_post.html'
    form_class = PostForm
    permission_required = ('news.add_post',)
    raise_exception = True

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.post_author = self.request.user
        fields.save()
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    from django.urls import reverse

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "text"]
    template_name = 'blog/post_edit.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return reverse('post_detail', args=[post.pk])

    
class PostUpdateView(UpdateView):
    model = Post
    fields = ["title","text"]
    template_name = 'blog/post_edit.html'
    
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name ='posts'

