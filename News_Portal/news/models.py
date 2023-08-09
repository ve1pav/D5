from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    autUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAut = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_sum = self.post_set.aggregate(postRating=Sum('rating'))
        temp_sum_p = 0
        temp_sum_p += post_sum.get('postRating')

        comment_sum = self.autUser.comment_set.aggregate(commentRating=Sum('rating'))
        temp_sum_c = 0
        temp_sum_c += comment_sum.get('commentRating')

        self.ratingAut = temp_sum_p * 3 + temp_sum_c
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGORY_CHOICES = (
        ('AR', 'Статья'),
        ('NW', 'Новость'),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    creationDate = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    content = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.content[:123]} ...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
