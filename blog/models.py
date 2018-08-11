import string
import random

from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.template import loader
from django.template.defaultfilters import urlencode


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Roboczy'),
        ('published', 'Opublikowany'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='published')
    author = models.ForeignKey(User, related_name='posts',
                               on_delete=models.CASCADE)
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='draft')

    objects = models.Manager()
    active = PublishedManager()

    def get_absolute_url(self):
        date = timezone.localdate(self.published)
        return reverse('blog:post_detail',
                       args=[date.year,
                             date.strftime('%m'),
                             date.strftime('%d'),
                             self.slug])

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return f'{self.title} by {self.author.username.title()}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status != 'published':
            return
        args = {
            'url': self.get_absolute_url(),
            'title': self.title,
            'host':  settings.DOMAIN,
        }
        for addr in NewsletterAddresse.objects.all():
            args['resign_link'] = addr.get_resign_link()
            msg = loader.render_to_string('email/post.html', args)
            send_mail(self.title, '', 'no-reply@piotrekczajka.pl',
                      [addr.email], fail_silently=False,
                      html_message=msg)


class NewsletterAddresse(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=60)

    def get_resign_link(self):
        email = urlencode(self.email)
        token = urlencode(self.token)
        return f'cancel-newsletter/{email}/{token}'

    def save(self, *args, **kwargs):
        alphabet = string.printable.replace('/', '')
        token = ''.join(random.choice(alphabet) for _ in range(60))
        self.token = token
        super().save(*args, **kwargs)
