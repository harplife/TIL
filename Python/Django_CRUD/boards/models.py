from django.db import models

# Create your models here.


class Board(models.Model):
    # id는 기본적으로 처음 테이블 생성시 자동으로 만들어진다.
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=16)
    content = models.TextField()
    # 데이터가 생성이 될 떄 auto_now_add
    created_at = models.DateTimeField(auto_now_add=True)
    # 데이터가 수정이 될 떄 auto_now
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}번째 글 - {self.title}'
