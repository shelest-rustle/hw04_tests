from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group
from django.contrib.auth import get_user_model
from .forms import PostForm
from django.contrib.auth.decorators import login_required


User = get_user_model()


# Create your views here.
def index(request):
    template = 'posts/index.html'
    posts = Post.objects.select_related('group').all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'posts': posts
    }
    return render(request, template, context)


def group_list(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author').all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    user_name = get_object_or_404(User, username=username)
    author_posts = user_name.posts.select_related('group', 'author')
    posts_count = author_posts.count()
    paginator = Paginator(author_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': user_name,
        'author_posts': author_posts,
        'page_obj': page_obj,
        'posts_count': posts_count
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    first_30 = post.text[:30]
    posts_count = post.author.posts.count()
    is_author = post.author == request.user

    context = {
        'post_id': post_id,
        'post': post,
        'first_30': first_30,
        'posts_count': posts_count,
        'is_author': is_author
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None)
    context = {
        'form': form,
    }

    if not form.is_valid():
        return render(request, template, context)

    form = form.save(commit=False)
    form.author = request.user
    form.save()
    return redirect('posts:profile', request.user.username)


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post.id)

    form = PostForm(request.POST or None, instance=post)
    context = {
        'form': form,
        'is_edit': True,
        'post_id': post_id
    }

    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()
        return redirect('posts:post_detail', post_id=post.id)

    return render(request, template, context)
