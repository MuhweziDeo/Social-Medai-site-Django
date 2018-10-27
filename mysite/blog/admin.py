from django.contrib import admin

# Register your models here.
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    # displays navbar for item
    list_filter = ('status', 'created', 'publish', 'author')
    # allow filtering of items
    search_fields = ('title', 'body')
    # search box
    prepopulated_fields = {'slug': ('title',)}
    # prepopluates slug field with title field
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    # add ordering
    ordering = ['status', 'publish']


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(Comment, CommentAdmin)
