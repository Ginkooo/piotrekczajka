import json
from validate_email import validate_email

from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages

from blog.forms import EmailPostForm
from blog.models import Post, NewsletterAddresse


class PostListView(ListView):
    queryset = Post.active.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, slug):
    post = Post.active.get(slug=slug,
                           published__year=year)

    return render(request, 'blog/post/detail.html', {'post': post})


def newsletter(request):
    email = json.loads(request.body)['email']
    valid = validate_email(email)
    if not valid:
        return JsonResponse({'msg': 'Invalid email'}, status=500)
    try:
        NewsletterAddresse.objects.create(email=email)
    except Exception:
        return JsonResponse({'msg': 'You have already signed :)'}, status=500)
    return JsonResponse({'msg': 'Successfully signed for newsletter!'})


def cancel_newsletter(request, email, token):
    obj = get_object_or_404(NewsletterAddresse, email=email, token=token)
    obj.delete()
    messages.add_message(request, messages.INFO,
                         f'Sucessfully removed {email} from newsletter list')
    return render(request, 'blog/post/list.html')
