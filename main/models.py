from django.urls import reverse
from django.db import models
from accounts.models import CustomUser


class Author(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='author')

    @property
    def count_posts(self):
        return self.Articles.all().count()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Авторство'
        verbose_name_plural = 'Авторы'


class Ip(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Tags(models.Model):
    tag_name = models.CharField(max_length=255)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Article(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='author_articles')
    published_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    image_url = models.ImageField(upload_to='media', blank=True)
    tags = models.ManyToManyField(Tags)

    @property
    def count_like(self):
        return self.article_likes.all().count()

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Likes(models.Model):
    who_likes = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_likes')
    count_of_likes = models.PositiveSmallIntegerField(default=0)
    when_liked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.who_likes} лайкнул: {str(self.article)}"

    class Meta:
        verbose_name = 'Лайки'
        verbose_name_plural = 'Лайков'


class Comments(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class CommentLikes(models.Model):
    who_likes = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name='comment_likes')
    count_of_likes = models.PositiveSmallIntegerField(default=0)
    when_liked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.who_likes} лайкнул комментарий: {str(self.comment)}"

    class Meta:
        verbose_name = 'Лайки комментариев'
        verbose_name_plural = 'Лайк комментария'


class PageHit(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='page_hit')
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.article)

    class Meta:
        verbose_name = 'Просмотры'
        verbose_name_plural = 'Просмотров'
