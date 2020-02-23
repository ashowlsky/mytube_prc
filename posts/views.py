from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Group, User, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from users.models import Profile, Relations, Logout_time_records
import datetime as dt
from django.dispatch import receiver



def index(request):
    username = request.user.username
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'username':username})

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group = group).order_by("-pub_date")[:12]
    return render(request, "group.html", {"group":group, "posts":posts})

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
    user = get_object_or_404(User, username=username)
    current_user = request.user
    """ Добавил проверку подписки на автора, чей профиль просматривается
    чтобы показывать дату начала подписки. Все остальное также как в основном проекте."""
    relation_started = None
    if Relations.objects.filter(follower_id=current_user.id, following_id=user.id).exists():
        relation = Relations.objects.get(follower_id=current_user.id, following_id=user.id)
        relation_started = relation.started_on
    following = True if Relations.objects.filter(follower=current_user, following=user).exists() else False
    post_list = user.posts.order_by("-pub_date").all()
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number) 
    return render(request, "profile.html", {"user":user, 'page':page, 'following':following, 'relation_started':relation_started})
     

def post_view(request, username, post_id):
    """ На странице поста можно сразу добавлять комментарии. Еще добавил в модель Post
    поле is_read, false по дефолту, для проверки был ли пост прочитан. Тег 'New!' (описан в функции 'feed') убирается когда
    пользователь зайдет на страницу поста."""
    post = Post.objects.get(id=post_id)
    post.is_read = True
    post.save()
    comments = post.comments.order_by('-pub_date').all()
    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number)
    add_comment_form = CommentForm(request.POST)
    if add_comment_form.is_valid():
        comment = add_comment_form.save(commit=False)
        comment.related_post = post
        comment.comment_author = request.user
        comment.save()
        return redirect('post', username=username, post_id = post_id)
    add_comment_form = CommentForm()
    return render(request, 'post.html', {"add_comment_form":add_comment_form, "post":post, "page":page})


def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    update_indicator = True
    current_user = request.user
    if current_user == post.author:
        form = PostForm(request.POST or None, instance = post)
        if form.is_valid():
            form.save()
            return redirect('post', username=username, post_id = post.id)
        return render(request, 'new.html', {'form':form, 'update_indicator':update_indicator})
    return render(request, "new.html", {"form":form, 'update_indicator':update_indicator})

@login_required
def like(request):
    """ Живут в модели Post в m2m поле. В поле записываются пользователи. Если пользователь там есть,
    то повторный клик его уберет. Нажатие на дислойс убирает лойс. Тут у меня есть вопросы... """
    username = request.user.username
    post = get_object_or_404(Post, id=request.POST['post_id'])
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        post.dislikes.remove(request.user)
    return redirect(f'/{username}/{post.id}/')
     

@login_required
def dislike(request):
    """ Работают также как и Like """
    username = request.user.username
    post = get_object_or_404(Post, id=request.POST['post_id'])
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        post.likes.remove(request.user)
    return redirect(f'/{username}/{post.id}/')

@login_required
def feed(request, username):
    """Чужой фид смотреть нельзя. Реализация запроса к базе ужасна. В объекте модели Relations
    нахожу id авторов на которых подписан пользователь. Потом достаю самих авторов. Сначала делаю список постов каждого автора.
    А потом каждый пост отдельно переношу в окончательный список. Ищу как реализовать это короче. В users.models есть ресивер,
    который регистрирует момент выхода пользователя. Если кто-то, на кого подписан пользователь создаст пост во время его отсутствия, то у такого поста
    в ленте будет тег 'New!'. """
    if request.user.username != username:
        return redirect('index')
    user = request.user
    logout_flag = Logout_time_records.objects.get(user=user)
    last_logged = logout_flag.last_logout_time
    id_pool = [relation.following_id for relation in user.follows.all()]
    authors = [User.objects.get(id=i) for i in id_pool]
    posts = []
    for a in authors:
        posts_a = a.posts.all()
        for post in posts_a:
            posts.append(post)
    for post in posts:
        if post.pub_date > last_logged:
            post.is_new = True
            post.save()
    return render(request, 'feed.html', {"posts":posts})