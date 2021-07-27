from django.contrib.auth.decorators import login_required
import re
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Comment, Post
from appuser.models import UserModel
from .forms import PostForm
from notification.models import LikeNotification, Notification


def PostLike(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        post.liked = False
    else:

        liked = LikeNotification.objects.create(


            liked=request.user,
            post=post
        )

        Notification.objects.create(

            receiver=post.author,
            delete_like=liked.id,
            liked=liked
        )
        post.likes.add(request.user)
        post.liked = True
    post.save()

    return redirect(request.META.get('HTTP_REFERER',
                                     'redirect_if_referer_not_found'))


def CommentLike(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        comment.liked = False
    else:
        comment.likes.add(request.user)
        comment.liked = True
    comment.save()

    return redirect(request.META.get('HTTP_REFERER',
                                     'redirect_if_referer_not_found'))


def post(request):

    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('login'))
    count = len(
        [notified for notified in Notification.objects.filter(
            receiver__id=request.user.id)])

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            at = re.findall(r'@([\w]+)', data.get("text"))

            new_post = Post.objects.create(
                text=data['text'],
                post_content=data['post_content'],
                author=request.user
            )
        if at:
            for a in at:
                user = UserModel.objects.filter(username=a)
                if not user:
                    return HttpResponseRedirect(reverse('homepage'))
                if request.user != UserModel.objects.get(username=a):

                    Notification.objects.create(
                        post=new_post,
                        receiver=UserModel.objects.get(username=a),
                        delete_id=new_post.id
                    )

        return HttpResponseRedirect(reverse('homepage'))

    form = PostForm()

    return render(request, 'generic_form.html', {'form': form, 'count': count})


# def comment(request, post_id):
#     # def commentNotification(reciever):
#     #     Notification.objects.create(
#     #         comment=new_comment,
#     #         receiver=reciever,
#     #         delete_comment=new_comment.id
#     #     )
#     if request.method == 'POST':
#         form = PostForm(request.POST)

#         if form.is_valid():
#             data = form.cleaned_data
#             post = Post.objects.get(id=post_id)
#             at = re.findall(r'@([\w]+)', data.get("text"))

#             new_comment = Comment.objects.create(
#                 replied_to=post,
#                 comment=data['text'],
#                 author=request.user
#             )

    # post.commenters.add(request.user)

    # for user in post.commenters.all():
    #     if user != request.user:

    #         commentNotification(user)

    # if at:
    #     for a in at:
    #         user = UserModel.objects.filter(username=a)
    #         if not user:
    #             pass
    #         else:

    #             reciever = UserModel.objects.get(username=a)
    #             if request.user != reciever:

    #                 commentNotification(reciever)

    #     return HttpResponseRedirect(reverse('homepage'))

    # form = PostForm()

    # return render(request, 'generic_form.html', {'form': form})

@login_required
def index(request):
    filt_post = Post.objects.filter(author=request.user)
    following_post = Post.objects.filter(
        author__in=request.user.following.all())
    following_post = filt_post | following_post
    following_post = following_post.order_by('-created_at')
    post = Post.objects.all().order_by('-created_at')
    comment = Comment.objects.all().order_by('-created_at')
    count = len(
        [notified for notified in Notification.objects.filter(
            receiver__id=request.user.id)])

    return render(
        request, 'post_test.html', {
            'post': post,
            "count": count,
            'comment': comment,
            'following_post': following_post,
            'filt_post': filt_post
        })

# def home_post(request):
#     post = Post.objects.all().order_by('-created_at')
#     comment = Comment.objects.all().order_by('-created_at')
#     count = len(
#     [notified for notified in Notification.objects.filter(
#         receiver__id=request.user.id)])
#     return render(request, 'index.html', {'post': post, 'comment': comment, 'count': count})


def PostDetailView(request, post_id):
    count = len(
        [notified for notified in Notification.objects.filter(
            receiver__id=request.user.id)])

    model = Post.objects.filter(id=post_id)
    comment = Comment.objects.all().order_by('-created_at')
    # template_name = MainApp/BlogPost_detail.html
    # context_object_name = 'object'
    return render(request, "post_test.html", {'post': model,
                                              'comment': comment, 'count': count})


def Test_view(request):
    def commentNotification(reciever):
        Notification.objects.create(
            comment=new_comment,
            receiver=reciever,
            delete_comment=new_comment.id,

        )
    tested = request.POST.dict()
    at = re.findall(r'@([\w]+)', tested['comment'])
    post = Post.objects.get(pk=int(tested['post_id']))
    if post.author not in post.commenters.all():

        post.commenters.add(post.author)

    if request.user not in post.commenters.all():

        post.commenters.add(request.user)

    new_comment = Comment.objects.create(
        replied_to=post,
        comment=tested['comment'],
        author=request.user,
    )

    for user in post.commenters.all():
        if user != request.user:
            commentNotification(user)
        if at:
            for a in at:
                user = UserModel.objects.filter(username=a)
                if not user:
                    pass
                else:
                    reciever = UserModel.objects.get(username=a)
                    if request.user != reciever:

                        commentNotification(reciever)

    return redirect(request.META.get('HTTP_REFERER',
                                     'redirect_if_referer_not_found'))


def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk).delete()

    return redirect(request.META.get('HTTP_REFERER',
                                     'redirect_if_referer_not_found'))


def delete_comments(request, pk):
    comment = get_object_or_404(Comment, id=pk).delete()
    return redirect(request.META.get('HTTP_REFERER',
                                     'redirect_if_referer_not_found'))
