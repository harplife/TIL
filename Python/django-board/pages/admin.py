from django.contrib import admin
from .models import Post

# Register your models here.


@admin.register(Post) # admin.site.register(Post)를 대체한다
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'updated_at', )
    readonly_fields = ['created_at', 'updated_at', ] # admin페이지에서 볼수 있게 설정


