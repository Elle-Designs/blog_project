from django.shortcuts import render, redirect, get_object_or_404

from .models import BlogPost

from django.contrib.auth.decorators import login_required

# Create your views here.

def post_list(request):
    posts = BlogPost.objects.all().order_by('created_at')
    return render(request, 'appone/post_list.html', {'posts': posts})

@login_required
def post_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)
    return render(request, 'appone/post_detail.html', {'post': post})

@login_required
def post_create(request):
   if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        post = BlogPost.objects.create(title=title, content=content, author=request.user)

        return redirect('post_detail', id=post.id)
   return render(request, 'appone/post.html')

@login_required
def post_update(request, id):
    post = get_object_or_404(BlogPost, id=id)
    if post.author != request.user:
        return redirect('post_detail')
    
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        post.save()
        return redirect('post_detail', id=post.id)
    return render(request, 'appone/post.html', {'post': post})

@login_required
def post_delete(request, id):
    post = get_object_or_404(BlogPost, id=id)
    if post.author == request.user:
        post.delete()
    return redirect('post_list')
    
