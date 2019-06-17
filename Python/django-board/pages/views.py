from django.shortcuts import render, redirect, get_object_or_404
from pages.models import Post
from django.views.decorators.http import require_http_methods, require_GET

# Create your views here.


@require_GET
def index(request):
    posts = Post.objects.order_by('-pk')
    context = {'posts': posts}
    return render(request, 'pages/index.html', context)

