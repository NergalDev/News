#from datetime import datetime
#from resourses import TYPE_POST
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#article = 'AR'
#news = 'NW'
#TYPE_POST = [
#    (article, 'статья')
#    (news, 'новость')
#]

#class User(AbstractUser):
   # username = models.CharField(max_length=20, unique=True)
    #email = models.EmailField(_('email adress', unique=True))
   # password = models.CharField(max_length=255)
    #registration = models.DateField(auto_now_add=True)

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = 0
        for post in self.post_set.all():
            self.rating += post.rating * 3
            for other_comment in post.comment_set.exclude(author__username=self.user.username):
                self.rating += other_comment.rating
        for comment in self.user.comment_set.all():
            self.rating += comment.rating
        self.save()

class Category(models.Model):
    category_name = models.CharField(max_length=25, unique=True)


class Post(models.Model):
    post_type = models.CharField(max_length=2, choices=TYPE_POST)
    post_tytle = models.CharField(max_length=100)
    post = models.TextField()
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_creations = models.DateTimeField(auto_now_add=True)
    post_rating = models.IntegerField(default=0, db_column='post_rating')
    #post_rating = models.IntegerField(default=0)



    @property
    def get(self):
        return self.post_rating

    def like(self):
        self.post_rating += 1
        Post.objects.filter(id=self.id).values('post_rating').update(post_rating='post_rating' + self.post_rating)


    @like_post.setter
   # def like(self):
    #    self.post_rating =
    def update_rating(self):
        post_rating = sum(Post.objects.filter(author=self.user).values('post_rating')) * 3
        comment_auth_rating = sum(Comment.objects.filter(user=self.user).values('comment_rating'))
        comment_post_rating = 0
        post_auth = Post.objects.filter(author=self.user).values('id')
        for id in post_auth:
            comment_post_rating += sum(Comment.objects.filter(post=id).values('comment_rating'))
        self.author_rating = post_rating + comment_auth_rating + comment_post_rating
        Author.objects.filter(id=self.id).values('Author_rating').update(author_rating = self.author_rating)

class PostCategory(models.Model):
    with_post = models.ForeignKey(to='Post', on_delete=models.CASCADE)
    with_category = models.ForeignKey(to='Category', on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField('Timestamp ', auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self, amount=1):
        self.rating += amount
        self.save()

    def dislike(self):
        self.like(-1)

    def __str__(self):
        return f'{self.author}: {self.text}'


