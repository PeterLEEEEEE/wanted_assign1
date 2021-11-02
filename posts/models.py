from django import db
from django.db import models
from core.models import TimeStamp
from users.models import User


class Category(TimeStamp):
    name = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = 'categories'

class Post(TimeStamp):
    title      = models.CharField(max_length=100, null=False)
    content    = models.TextField(null=False)
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0, verbose_name='게시글 조회수')
    category   = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'posts'