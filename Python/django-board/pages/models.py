from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.conf import settings

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    # image = models.ImageField(blank=True) # 해당 필드에 null값이 들어가도 된다
    image = ProcessedImageField(
        upload_to='pages/images', # 저장위치 (media 이후의 경로)
        processors=[Thumbnail(200, 300)],
        format='JPEG',
        options={'quality': 90},
        # 여기 안에 설정은 바로 적용되니 수정후 따로 makemigrations 할 필요 없다
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # django의 user 모델을 참조한다
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}. {self.title}'
