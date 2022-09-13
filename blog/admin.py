from django.contrib import admin

from .models import Author, Category, Post, Tag

admin.site.register([Author, Category, Post, Tag])
