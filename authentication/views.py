from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.contrib import messages

from post.models import Post, Comment
from authentication.forms import CreateUserForm, LoginForm
from appuser.models import UserModel


class CreateUser(View):
    def get(self, request):
        template = 'generic_form.html'
        form = CreateUserForm()
        return render(request, template, {'form': form, 'header': 'Signup'})

    def post(self, request):
        form = CreateUserForm(request.POST)
        print(form.errors)
        if form.is_valid():
            data = form.cleaned_data
            UserModel.objects.create_user(
                username=data.get('username'),
                password=data.get('password1')
            )
        return HttpResponseRedirect(reverse('login_page'))


class LoginUser(View):
    def get(self, request):
        template = 'generic_form.html'
        form = LoginForm()
        return render(request, template, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            my_user = authenticate(
                request, username=data['username'], password=data['password'])
            if my_user:
                login(request, my_user)
                post = Post.objects.all()
                for i in post:
                    if i.likes.filter(id=request.user.id):
                        i.liked = True
                    else:
                        i.liked = False
                    i.save()
                comment = Comment.objects.all()
                for i in comment:
                    if i.likes.filter(id=request.user.id):
                        i.liked = True
                    else:
                        i.liked = False
                    i.save()
                return HttpResponseRedirect(reverse('homepage'))
            else:
                messages.error(request, 'Username or password not correct')
                return redirect('login_page')
        form = LoginForm()
        return render(request, 'generic_form.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
