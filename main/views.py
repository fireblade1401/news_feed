from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView
from .models import Article, Category, Likes, Comments, PageHit, CommentLikes
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, CategoryForm, TagForm, CommentForm
from django.http import Http404, HttpResponseRedirect, JsonResponse


def index(request):
    articles = Article.objects.all()
    categories = Category.objects.all()
    context = {
        'article_list': articles,
        'categories': categories
    }
    return render(request, 'main/index.html', context)


@login_required
def get_article_by_category(request, category_id):
    articles = Article.objects.filter(category__id=category_id)
    categories = Category.objects.all()
    context = {
        'article_list': articles,
        'categories': categories
    }
    return render(request, 'main/index.html', context)


@login_required
def get_article_by_tag(request, tag_id):
    articles = Article.objects.filter(tags__id=tag_id)
    categories = Category.objects.all()
    context = {
        'article_list': articles,
        'categories': categories
    }
    return render(request, 'main/index.html', context)


def detail_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    page_hit, created = PageHit.objects.get_or_create(article=article)
    page_hit.count += 1
    page_hit.save()

    user_has_liked = Likes.objects.filter(who_likes=request.user, article=article).exists()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user.author
            comment.save()
            return redirect('article_detail', article_id)
    else:
        form = CommentForm()

    context = {
        'article': article,
        'form': form,
        'user_has_liked': user_has_liked,
        'page_hit': page_hit,
    }

    return render(request, 'main/detail_article.html', context)


@login_required
def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('/')
    else:
        form = ArticleForm()

    context = {
        'form': form,
    }
    return render(request, 'main/add_article.html', context)


@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CategoryForm()

    context = {
        'form': form,
    }

    return render(request, 'main/add_category.html', context)


@login_required
def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TagForm()

    context = {
        'form': form,
    }

    return render(request, 'main/add_tag.html', context)


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'main/edit_article.html'
    form_class = ArticleForm


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = '/'
    template_name = 'main/delete_article.html'


@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def delete_comment(request, comment_id):
    print("Inside delete_comment function")
    comment = get_object_or_404(Comments, id=comment_id)
    print(f"Found comment: {comment}")
    if request.user.author == comment.user:
        print("User matches, deleting comment")
        comment.delete()
        print("Comment deleted")

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
def like_article(request, article_id):
    article = Article.objects.get(pk=article_id)
    user_has_liked = Likes.objects.filter(who_likes=request.user, article=article).exists()
    existing_like = Likes.objects.filter(who_likes=request.user, article=article).first()

    if user_has_liked:
        existing_like.delete()
    else:
        new_like = Likes(who_likes=request.user, article=article, count_of_likes=1)
        new_like.save()

    return HttpResponseRedirect(reverse('article_detail', args=[article_id]))


@login_required
def like_comment(request, comment_id):
    comment = Comments.objects.get(pk=comment_id)
    user_has_liked = CommentLikes.objects.filter(who_likes=request.user, comment=comment).exists()
    existing_like = CommentLikes.objects.filter(who_likes=request.user, comment=comment).first()

    if user_has_liked:
        existing_like.delete()
    else:
        new_like = CommentLikes(who_likes=request.user, comment=comment, count_of_likes=1)
        new_like.save()

    return HttpResponseRedirect(reverse('article_detail', args=[comment.article.id]))


