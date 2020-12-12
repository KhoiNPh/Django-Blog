# from django.views import generic
from .models import Post, Comment, Message
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm1, CommentForm2, PostCreateForm, PostEditForm, UserLoginForm, MessageForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.models import User
# from django.core.mail import send_mail


def post_list(request):
    template_name = 'index.html'
    posts = Post.objects.filter(status=1).order_by('-created_on')
    p = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        post_list = p.page(page)
    except PageNotAnInteger:
        post_list = p.page(1)
    except EmptyPage:
        post_list = p.page(p.num_pages)

    if page is None:
        start_index = 0
        end_index = 5
    else:
        (start_index, end_index) = proper_pagination(post_list, index=3)

    page_range = list(p.page_range)[start_index:end_index]
    sidebar_list = Post.objects.filter(status=1).order_by('-created_on')[:6]

    return render(request, template_name, {'post_list': post_list,
                                           'sidebar_list': sidebar_list,
                                           'page_range': page_range})


def proper_pagination(post_list, index):
    start_index = 0
    end_index = 5
    if post_list.number > index:
        start_index = post_list.number - index
        end_index = post_list.number + index - 1

    return (start_index, end_index)


def post_detail(request, _slug):
    template_name = 'post_detail.html'
    post = Post.objects.get(slug=_slug)
    comments = Comment.objects.filter(post=post).order_by('-created_on')
    sidebar_list = Post.objects.filter(status=1).order_by('-created_on')[:6]

    if request.method == 'POST':
        comment_form = CommentForm2(data=request.POST)
        if comment_form.is_valid():

            body = request.POST.get('body')
            reply_id = request.POST.get('comment_id')
            comment_qs = None

            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)

            if request.user.is_authenticated:
                name = request.user.username
            else:
                name = request.POST.get('name')

            comment = Comment.objects.create(
                post=post, name=name, body=body, reply=comment_qs)
            comment.save()
            # return HttpResponseRedirect(post.get_absolute_url())
    else:
        if request.user.is_authenticated:
            comment_form = CommentForm2()
        else:
            comment_form = CommentForm1()

    if request.is_ajax():
        html = render_to_string('comment.html', {'post': post,
                                                 'comments': comments,
                                                 'comment_form': comment_form,
                                                 'sidebar_list': sidebar_list}, request=request)
        return JsonResponse({'form': html})

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'comment_form': comment_form,
                                           'sidebar_list': sidebar_list})


def blogger_list(request):
    template_name = 'about.html'
    blogger_list = Post.objects.filter(status=3)
    sidebar_list = Post.objects.filter(status=1).order_by('-created_on')[:6]

    return render(request, template_name, {'blogger_list': blogger_list,
                                           'sidebar_list': sidebar_list})


@login_required(login_url='/login/')
def post_create(request, user):
    template_name = 'post_create.html'

    if request.method == 'POST':
        postcreate_form = PostCreateForm(
            data=request.POST, files=request.FILES)
        if postcreate_form.is_valid():
            postcreate_form.save()
            post = postcreate_form.save(commit=False)
            post.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        postcreate_form = PostCreateForm()
    return render(request, template_name, {'postcreate_form': postcreate_form})


@login_required(login_url='/login/')
def post_edit(request, user, post_id):
    post = Post.objects.get(id=post_id)
    template_name = 'post_edit.html'

    if request.method == 'POST':
        postedit_form = PostEditForm(request.POST or None, instance=post)
        if postedit_form.is_valid():
            postedit_form.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        postedit_form = PostEditForm(instance=post)
    return render(request, template_name, {'postedit_form': postedit_form})


def user_login(request):
    template_name = 'login.html'
    if request.method == 'POST':
        userlogin_form = UserLoginForm(request.POST)
        if userlogin_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return HttpResponseRedirect(reverse('home'))
                else:
                    return HttpResponse("User is not active")
            else:
                HttpResponse("User is None")
    else:
        userlogin_form = UserLoginForm()

    return render(request, template_name, {'userlogin_form': userlogin_form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/login/')
def user_posts(request, user):
    template_name = 'user_posts.html'
    user_posts = Post.objects.filter(
        author=request.user).order_by('-created_on')

    return render(request, template_name, {'user_posts': user_posts})


@login_required(login_url='/login/')
def post_delete(request, user, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()

    return HttpResponseRedirect(reverse('user_posts', args=[user]))


def contact_message(request):
    template_name = 'contact.html'

    if request.method == 'POST':
        message_form = MessageForm(data=request.POST)
        if message_form.is_valid():
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            content = request.POST.get('content')
            message = Message.objects.create(
                email=email, content=content, subject=subject)
            message.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        message_form = MessageForm()
    return render(request, template_name, {'message_form': message_form})


@login_required(login_url='/login/')
def user_messages(request, user):
    template_name = 'user_messages.html'
    user_messages = Message.objects.filter(
        user_to_reply=request.user).order_by('is_read', '-created_on')
    return render(request, template_name, {'user_messages': user_messages})


@login_required(login_url='/login/')
def message_detail(request, user, message_id):
    template_name = 'message_detail.html'
    message = Message.objects.get(id=message_id)
    message.is_read = True
    message.save()

    return render(request, template_name, {'message': message})


@login_required(login_url='/login/')
def message_delete(request, user, message_id):
    message = Message.objects.get(id=message_id)
    message.delete()

    return HttpResponseRedirect(reverse('user_messages', args=[user]))


@login_required(login_url='/login/')
def message_markread(request, user, message_id):
    message = Message.objects.get(id=message_id)
    message.is_read = not message.is_read
    message.save()

    return HttpResponseRedirect(reverse('user_messages', args=[user]))


@login_required(login_url='/login/')
def message_forward(request, user, message_id):
    message = Message.objects.get(id=message_id)
    is_superuser = not request.user.is_superuser
    message.user_to_reply = User.objects.filter(is_superuser=is_superuser)[0]
    message.save()

    return HttpResponseRedirect(reverse('user_messages', args=[user]))


# @login_required(login_url='/login/')
# def message_reply(request, user, message_id):
#     template_name = 'message_reply.html'
#     message = Message.objects.get(id=message_id)
#     toemail = message.email

#     if request.method == 'POST':
#         mail_form = MailForm(data=request.POST)
#         if mail_form.is_valid():  
#             subject = request.POST.get('subject')
#             content = request.POST.get('content')
#             mail = Mail.objects.create(content=content, subject=subject, message=message)
#             mail.save()
#             send_mail(subject=subject, message=content, from_email='xxx@gmail.com',
#             recipient_list=[toemail], fail_silently=False,)
#             message.is_replied = True
#             message.save()
#             return HttpResponseRedirect(reverse('message_detail', args=[user, message_id]))
#     else:
#         mail_form = MailForm()
#     return render(request, template_name, {'mail_form': mail_form})


# class PostList(generic.ListView):
#     template_name = 'index.html'
#     model = Post
#     paginate_by = 4

#     def get_context_data(self, **kwargs):
#         context = super(PostList, self).get_context_data(**kwargs)
#         p = Paginator(Post.objects.filter(status=1).order_by('-created_on'), self.paginate_by)
#         context['post_list'] = p.page(context['page_obj'].number)
#         context['sidebar_list'] = Post.objects.filter(status=1).order_by('-created_on')[:6]

#         return context

# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super(PostDetail, self).get_context_data(**kwargs)
#         context['sidebar_list'] = Post.objects.filter(status=1).order_by('-created_on')[:6]

#         return context


# class BloggerList(generic.ListView):
#     template_name = 'about.html'
#     model = Post

#     def get_context_data(self, **kwargs):
#         context = super(BloggerList, self).get_context_data(**kwargs)
#         context['blogger_list'] = Post.objects.filter(status=3)
#         context['sidebar_list'] = Post.objects.filter(status=1).order_by('-created_on')[:6]

#         return context
