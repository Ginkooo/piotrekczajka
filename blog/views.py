from datetime import datetime

from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.utils import timezone

from blog.forms import EmailPostForm
from blog.models import Post


def post_share(request, id):
    post = get_object_or_404(Post, id=id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} ({cd["email"]}) zachęca do przeczytania '\
                      f'"{post.title}"'
            msg = f'Przeczytaj post "{post.title}" na stronie {post_url}\n\n'\
                  f'Komentarz dodany przez {cd["name"]}: {cd["comments"]}'
            send_mail(subject, msg,
                      'czajka@protonmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


class PostListView(ListView):
    queryset = Post.active.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, slug):
    post = Post.active.get(slug=slug,
                           published__year=year)
    # TODO:Why the hell is it not working?


    return render(request, 'blog/post/detail.html', {'post': post})
