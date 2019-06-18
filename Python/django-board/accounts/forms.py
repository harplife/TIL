from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserChangeForm(UserChangeForm):
    # 모델에 대한 정보가 담기는 곳
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', )
