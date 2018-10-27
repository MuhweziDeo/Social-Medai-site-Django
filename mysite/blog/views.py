from django.shortcuts import render, get_object_or_404
# Create your views here.
from .models import Post
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import EmailForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag


def post_list(request, tag_slug=None):
    posts = Post.published.all()
    # object_list = Post.published.all()
    # paginator = Paginator(object_list, 1)  # 3 posts per page
    # page = request.GET.get('page')
    # try:
    #     posts = paginator.page(page)
    # except PageNotAnInteger:
    #     posts = paginator.page(1)
    # except EmptyPage:
    #     # if page is out of range deliver last page of results
    #     posts = paginator.page(paginator.num_pages)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags_in=[tag])
    return render(request, 'blog/post/list.html', {

        'posts': posts,
        'tag': tag})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # return render(request, 'blog/post/detail.html', {'post': post})
    # list active comments
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        # a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create comment object but dont save it to database
            new_comment = comment_form.save(commit=False)
            # assign current post to the comment
            new_comment.post = post
            # save comment
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})


def post_share(request, pk):
    post = get_object_or_404(Post, id=pk, status='published')
    sent = False
    form = EmailForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        # post_url = request.build_absolute_uri(post.get_absolute_url())
        post_url = "url"
        subject = '{}({}) recomends you reading "{}"'.format(
            cd['name'], cd['email'], post_url)
        message = 'Read "{}" at {}\n\n{}\'s comments'.format(
            post.title, post_url, cd['comments'])
        send_mail = (subject, message, 'aggrey256@gmail.com', [cd['to']])
        sent = True
    else:
        form = EmailForm()
    return render(request, 'blog/post/share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent})
