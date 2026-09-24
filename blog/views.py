from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from .models import BlogPost

def post_list(request):
    posts = cache.get("all_blog_posts")
    if posts is None:
        posts = list(BlogPost.objects.filter(published=True))
        cache.set("all_blog_posts", posts, 120)
    return render(request, "blog/blogs.html", {"posts": posts})

def post_detail(request, slug):
    return render(request, "blog/blog_detail.html", {"post": get_object_or_404(BlogPost, slug=slug, published=True)})
