from django.contrib import admin

from apps.comments.models import Comment

from .models import Post, PostExtraImage


class PostExtraImageInline(admin.TabularInline):
    model = PostExtraImage
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = [PostExtraImageInline, CommentInline]


admin.site.register(Post, PostAdmin)
