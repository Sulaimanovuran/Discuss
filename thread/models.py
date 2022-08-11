from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='categories')
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(primary_key=True, max_length=100, unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subsidiary')

    def save(self, *args, **kwargs):
        self.slug = self.title.lower()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.slug}----------{self.owner}'
        else:
            return f'{self.slug}-------------{self.owner}'


class Thread(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='threads')
    name = models.CharField(max_length=500)
    category = models.ManyToManyField(Category, related_name='threads')
    cover = models.ImageField(upload_to='covers')

    def __str__(self):
        return f'{self.pk}______{self.name}______{self.author}'


class Answer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='answers')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text}'




class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Comment_Image(models.Model):
    image = models.ImageField(upload_to='images')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_images')


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='images')


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='likes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField('Like', default=False)


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ratings')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='ratings')
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(5)], default=1
    )


class Favourite(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='favorites')