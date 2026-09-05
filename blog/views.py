from django.shortcuts import get_object_or_404, render
from .models import BlogPost
def post_list(request): return render(request, "blog/blogs.html", {"posts": BlogPost.objects.filter(published=True)})
def post_detail(request, slug): return render(request, "blog/blog_detail.html", {"post": get_object_or_404(BlogPost, slug=slug, published=True)})
