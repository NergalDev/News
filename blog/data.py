import random
from .models import Author, User, Category, Post, Comment

users = [
    "Нил Деграсс Тайсон",
    "Карл Саган",
    "Андрей"
]

authors = users[:2]

categories = [
    "Астрофизика",
    "Новости",
    "Наука",
    "Технологии"
]

article_text = """ 
Профессор Neil deGrasse Tyson - Специализацией Тайсона является астрофизика - наука на границе физики
и астрономии, исследующая тайны строения, эволюции, химического состава и физических свойств небесных 
тел, изучающая Вселенную в целом. Она включает в себя специфические явления, часто невидимые невооруженным
глазом с Земли. Примерами являются звезды и галактики, а также законы, управляющие материей в космическом
пространстве. Нил Деграсс Тайсон специализируется на познании космоса, ищет ответы на самые насущные вопросы
человечества.

 """


def create_users():
    for name in users:
        User.objects.create_user(username=name)
    print(User.objects.all())


def create_authors():
    for name in authors:
        Author.objects.create(user=User.objects.get_by_natural_key(username=name))
    print(Author.objects.all())


def create_categories():
    for category in categories:
        Category.objects.create(name=category)
    print(Category.objects.all())


def create_articles():
    article_authors = Author.objects.all()
    post = Post.objects.create(author=article_authors[0], title="Первая статья", text=article_text)
    post.category.add(Category.objects.get(id=3), Category.objects.get(id=1))
    post = Post.objects.create(author=article_authors[1], title="Вторая статья", text=article_text)
    post.category.add(Category.objects.get(id=2), Category.objects.get(id=3))
    news = Post.objects.create(author=article_authors[1], title="Первая новость",
                               post_type=Post.NEWS, text=article_text)
    news.category.add(Category.objects.get(id=4), Category.objects.get(id=1))
    print(Post.objects.all())


def add_comments():
    users = User.objects.all()
    posts = Post.objects.all()
    for user in users:
        for post in posts:
            text = f"{user.username} {random.choice(['одобряет', 'осуждает'])}"
            Comment.objects.create(post=post, user=user, text=text)


def like_dislike_posts_and_comments():
    for post in Post.objects.all():
        action = random.choice([post.like, post.like, post.dislike])    # Повысим шанс положительной оценки
        action()
    for comment in Comment.objects.all():
        action = random.choice([comment.like, comment.like, comment.dislike])   # Повысим шанс положительной оценки
        action()


def update_ratings():
    for author in Author.objects.all():
        author.update_rating()


def print_ratings():
    print("\n======== Рейтинг авторов ==========")
    for author in Author.objects.all():
        print(f"{author.user.username}, rating={author.rating}")


def print_best_rating_author():
    top_rating_author = Author.objects.order_by('-rating').first()
    print("\n======== Автор с самым высоким рейтингом ==========")
    print(f"{top_rating_author.user.username}, rating={top_rating_author.rating}")


def print_best_rating_article():
    post = Post.objects.order_by('-rating').first()
    print("\n======== Статья с самым высоким рейтингом ==========")
    print(f"Дата добавления: {post.date_time}\n"
          f"Автор: {post.author.user.username}\n"
          f"Рейтинг статьи: {post.rating}\n"
          f"Заголовок: {post.title}\n"
          f"Превью: {post.preview(length=128)}")


print_ratings()
update_ratings()
print_ratings()
print_best_rating_author()
print_best_rating_article()
