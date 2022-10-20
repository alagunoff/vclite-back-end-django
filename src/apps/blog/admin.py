from django.contrib import admin

from .models.author import Author
from .models.category import Category
from .models.comment import Comment
from .models.post import Post, PostExtraImage
from .models.tag import Tag


class PostExtraImageInline(admin.TabularInline):
    model = PostExtraImage
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = [PostExtraImageInline, CommentInline]


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
