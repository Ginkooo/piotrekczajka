from django.contrib import admin
from blog.models import Post, NewsletterAddresse


class PostAdmin(admin.ModelAdmin):
    list_display = 'title slug author published status'.split()
    list_filter = 'status created published author'.split()
    search_fields = 'title body'.split()
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    ordering = 'status published'.split()


class NewsletterAddresseAdmin(admin.ModelAdmin):
    list_display = 'email token'.split()


admin.site.register(Post, PostAdmin)
admin.site.register(NewsletterAddresse, NewsletterAddresseAdmin)
