from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
import datetime

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import DetailView, UpdateView, DeleteView, View

from .forms import CommentForm, PostForm, ProfileForm, UserUpdateForm, ReplyForm, UserRegisterForm
from .models import Post, Profile, Comment
# Create your views here.
from .tokens import account_activation_token


def about_view(request):
    return render(request, 'milk\about.html')


def post_list(request):
    posts = Post.objects.filter(status=1).order_by('-created_on')
    date = datetime.datetime.now()
    context = {'posts': posts, 'current_date': date}
    return render(request, 'milk/post_list.html', context)


def post_detail(request, slug):
    template_name = 'milk/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all
    context = {'post': post, 'slug': slug, 'comments': comments}
    return render(request, template_name, context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'milk/post_form.html', context)


class PostUpdate(UpdateView):
    model = Post
    form = PostForm
    fields = ['title', 'content', 'post_pic']


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('home')


@login_required
def comment_create(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.name = request.user 
            comment.dp = request.user.profile.dp.url
            comment.save()
            return HttpResponseRedirect(reverse('post_detail', kwargs={'slug': slug}))
    else:
        form = CommentForm()
    context = {'form': form, 'post': post}
    return render(request, 'milk/comment_form.html', context)


class CommentUpdate(UpdateView):
    model = Comment
    fields = ['body']


class CommentDelete(DeleteView):
    model = Comment
    success_url = reverse_lazy('home')


@login_required
def profile_detail(request, pk):
    user = User.objects.get(pk=pk)
    context = {'user': user}
    return render(request, 'milk/profile_detail.html', context)


# the decorator: To access the profile page, users should login
@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return HttpResponseRedirect(reverse('profile_detail', kwargs={'pk': request.user.id}))

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'u_form': user_form,
        'p_form': profile_form
    }

    return render(request, 'milk/profile_update.html', context)


@login_required
def comment_detail(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    replies = comment.replies.all
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.name = request.user
            reply.dp = request.user.profile.dp.url
            reply.save()
            return HttpResponseRedirect(reverse('comment_detail', kwargs={'pk':pk}))
    else:
        form = ReplyForm()
    context = {'form': form, 'comment': comment, 'replies': replies, }
    return render(request, 'milk/comment_detail.html', context)


class SignUpView(View):
    form_class = UserRegisterForm
    template_name = 'milk/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, 'Please Confirm your email to complete registration.')

            return redirect('login')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')

