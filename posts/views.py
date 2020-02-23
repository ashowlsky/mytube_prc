from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Group, User
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10) # показывать по 10 записей на странице.
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number) # получить записи с нужным смещением
    return render(request, 'index.html', {'page': page, 'paginator': paginator})

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group = group).order_by("-pub_date").all()
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group":group, "post_list":post_list, "page":page, 'paginator': paginator})

@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'new.html', {'form':form})
    form = PostForm()
    return render(request, 'new.html', {'form':form})

def profile(request, username):
    author = get_object_or_404(User, username=username)

    """
    Это, почему-то, не проходит тесты, хотя отображается корректно.
    Из-за еще одной переменной в контексте?
    _______________________________________________________________

    latest = author.posts.latest("pub_date")
    post_list = author.posts.order_by("-pub_date")[1:]
    """
    post_list = author.posts.order_by("-pub_date")
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number) 
    return render(request, "profile.html", {"author":author, 'page':page, 'paginator': paginator})
     

def post_view(request, username, post_id):
    post = Post.objects.get(id=post_id)
    author = get_object_or_404(User, username=username)
    return render(request, "post.html", {"post":post, "author":author})

@login_required
def post_edit(request, username, post_id):
    update_indicator = True
    post = Post.objects.get(id=post_id)
    current_user = request.user
    if current_user != post.author:
        return redirect('post', username=username, post_id=post.id )
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post', username=username, post_id=post.id)
        return render(request, 'new.html', {"form":form, "update_indicator":update_indicator, "post":post})
    form = PostForm(instance=post)
    return render(request, "new.html", {"form":form, "update_indicator":update_indicator, "post":post})
    
