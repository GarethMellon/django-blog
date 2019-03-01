from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import BlogPostForm

# Create your views here.
def get_posts(request):
    """ Create a view that will reuten a list of posts that where published pior to now and render them to a template called 'blogposts.html'"""
    
    posts = Post.object.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blogposts.html', {'posts': posts})
    
def post_detail(request, pk):
    """ create a view that returns a single Post object based on the post ID and render to a template called 'postdetail.html' 
        or return 404 if not found
    """
    post= get_object_or_404(Post, pk=pk)
    post.view += 1
    post.save()
    return render(request, 'postdetail.html', {'post':post})
    
def create_or_edit_a_post(request, pk=None):
    """ creat a view that allows us to create or edit a post depending if the POST ID is null or now """
    
    post = get_object_or_404(Post, pk=pk) if pk else None
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, "blogpostsform.html", {'form':form})