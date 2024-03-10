from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Comment
from django.views.generic import ListView

from .forms import CommentForm
from django.views.decorators.http import require_POST

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post,
                                                    'form': form,
                                                    'comment': comment})

class PostListView(ListView):
 queryset = Post.published.all()
 context_object_name = 'posts'
 paginate_by = 3
 template_name = 'blog/post/list.html'

# Create your views here.
def post_list(request):
    posts_list = Post.published.all()
    paginator = Paginator(posts_list, 2)
    page_number = request.GET.get('page',1)
    posts =paginator.page(page_number)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(1)
    return render(request, 'blog/post/list.html', {"posts": posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, 
                            status=Post.Status.PUBLISHED,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day,
                            slug=post)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request, 'blog/post/detail.html', {"post": post,
                                                     'comments': comments,
                                                     'form': form})

def index(request):
    return HttpResponse('<h1>My first http response</h1>')


def hello(request):
    return HttpResponse("Hello<br>World!!!")
