from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CreationForm, ManageUserProfileForm, ManageUserForm
from django.core.mail import send_mail
from .models import User, Relations
from django.contrib.auth.decorators import login_required

class SignUp(CreateView):
    form_class = CreationForm
    success_url = "/auth/login/"
    template_name = "signup.html"

@login_required
def manage_user_profile(request):
    user = request.user
    if request.method == "POST":
        pic_form = ManageUserProfileForm(request.POST, request.FILES, instance=user.profile)
        pro_form = ManageUserForm(request.POST, instance=user)
        if pic_form.is_valid() and pro_form.is_valid():
            profile_pic = pic_form.save()
            pro = pro_form.save()
            return redirect('profile', username=user.username)
        return render(request, "manageuserprofile.html", {"pic_form":pic_form, "pro_form":pro_form})
    pic_form = ManageUserProfileForm(instance=user.profile)
    pro_form = ManageUserForm(instance=user)
    return render(request, "manageuserprofile.html", {"pic_form":pic_form, "pro_form":pro_form})

@login_required
def follow(request):
    #follower
    user = request.user
    #following
    username_user_to_follow = request.POST['follow_username']
    user_to_follow = get_object_or_404(User, username=username_user_to_follow)
    #check if a relationship exists
    if Relations.objects.filter(follower=user, following=user_to_follow).exists():
        return redirect(f'/{username_user_to_follow}/')
    else:
        Relations.objects.create(follower=user, following=user_to_follow)
        return redirect(f'/{username_user_to_follow}/')

def unfollow(request):
    #same pattern as follow
    user = request.user
    username_user_to_unfollow = request.POST['unfollow_username']
    user_to_unfollow = get_object_or_404(User, username=username_user_to_unfollow)
    if Relations.objects.filter(follower=user, following=user_to_unfollow).exists():
        Relations.objects.filter(follower=user, following=user_to_unfollow).delete()
        return redirect(f'/{username_user_to_unfollow}/')
    else:
        return redirect(f'/{username_user_to_unfollow}/')



