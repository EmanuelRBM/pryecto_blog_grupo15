from django.contrib import admin
from django.db import models

# Esta clase nos permite filtrar contenido en la admin

from .models import Post, Tag, Comment, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_on', 'updated_on')
    list_filter = ('tags', 'created_on', 'updated_on')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)} # Esto crea el enlace que luego se muestra en el navegador
    autocomplete_fields = ('tags',)

admin.site.register(Post, PostAdmin)


class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(Tag, TagAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display=('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'content')

admin.site.register(Comment, CommentAdmin)

admin.site.register(Category)