from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='img/avatars')
    nickname = models.CharField(max_length=100)

    objects = models.Manager()


class Tag(models.Model):
    name = models.CharField(max_length=100)

    objects = models.Manager()


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)

    objects = models.Manager()

    def __str__(self):
        return self.title


class QuestionRatingPoint(models.Model):
    LIKE = 'l'
    DISLIKE = 'd'

    TYPE_CHOICES = (
        (LIKE, 'like'),
        (DISLIKE, 'dislike'),
    )

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    is_correct = models.BooleanField(default=False)

    objects = models.Manager()


class CommentRatingPoint(models.Model):
    LIKE = 'l'
    DISLIKE = 'd'

    TYPE_CHOICES = (
        (LIKE, 'like'),
        (DISLIKE, 'dislike'),
    )

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
