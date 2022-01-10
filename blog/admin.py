from django.contrib import admin
from .models import Post, Comment


# admin for blogs.
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'title',
        'body',
        'intro',
        'timestamp',
    )

    read_only = ('slug',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)