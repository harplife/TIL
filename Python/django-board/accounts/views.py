from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET, require_http_methods


# Create your views here.

@require_http_methods(['GET', 'POST'])
def register(request):
    if request.user.is_authenticated:
        return redirect('pages:index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('pages:index')
    else:  # GET accounts/register
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('pages:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'pages:index')
    else:
        form = AuthenticationForm(request.POST)
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


@require_GET
def logout(request):
    auth_logout(request)
    return redirect('pages:index')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request):
    if not request.user.is_authenticated:
        return redirect('pages:index')

    if request.method == "POST":
        # 업뎃 로직 수행
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('pages:index')
    else:
        form = CustomUserChangeForm(instance=request.user)

    context = {'form': form}
    return render(request, 'accounts/update.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def chgPass(request):
    if request.method == 'POST':
        # 비번 변경 로직
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # 세션값과 회원정보가 달라져서
            # 세션을 유지한 상태로 새롭게 세션값을 업데이트 한다
            update_session_auth_hash(request, request.user)
            return redirect('pages:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'accounts/chgPass.html', context)


@require_POST
def delete(request):
    # 유저 삭제 로직
    request.user.delete()
    return redirect('pages:index')
