from django.contrib import admin

from thread.models import Category, Thread, Answer, Image, Comment, Like, Rating, Comment_Image, Favourite

admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Comment_Image)


class ThreadWithImage(admin.ModelAdmin):
    list_display = ['id', 'author', 'name', 'cover']


admin.site.register(Thread, ThreadWithImage)


class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ['image']
    max_num = 3


class AnswerWithImage(admin.ModelAdmin):
    inlines = [ImageInAdmin]
    list_display = ['id', 'created_at', 'thread', 'owner', 'text']


class CommentImageInAdmin(admin.TabularInline):
    model = Comment_Image
    fields = ['image']
    max_num = 2


class CommentWithImage(admin.ModelAdmin):
    inlines = [CommentImageInAdmin]
    list_display = ['id', 'created_at', 'owner', 'text', 'answer']


class Like1(admin.ModelAdmin):
    list_display = ['id', 'owner', 'answer', 'like']


class Rating1(admin.ModelAdmin):
    list_display = ['id', 'owner', 'answer', 'rating']


admin.site.register(Answer, AnswerWithImage)
admin.site.register(Comment, CommentWithImage)
admin.site.register(Like, Like1)
admin.site.register(Rating, Rating1)
admin.site.register(Favourite)