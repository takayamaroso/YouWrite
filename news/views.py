from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm, CommentForm, Search
from .models import Article, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import ListView
from django.db.models import Avg, Count
# Create your views here.

#－－－－－－－－記事リスト－－－－－－－－－－
def article_list(request):
    #検索窓の内容の検知
    if request.GET.get('search') is None:
        article_list = Article.objects\
            .filter(published_date__lte=timezone.now())\
            .annotate(avg_value=Avg('comments__evaluation_value'))\
            .order_by('-published_date')
    else:
        article_list = Article.objects\
            .filter(published_date__lte=timezone.now())\
            .filter(title__contains=request.GET.get('search'))\
            .annotate(avg_value=Avg('comments__evaluation_value'))\
            .order_by('-published_date')
    paginator = Paginator(article_list, 10) #ページ表示数
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages) #ページが範囲外の時最終ページを表示する
    return render(request, 'news/article_list.html', {'articles':articles})

#投稿順
def article_oldlist(request):
    #検索窓の内容の検知
    if request.GET.get('search') is None:
        article_list = Article.objects\
            .filter(published_date__lte=timezone.now())\
            .annotate(avg_value=Avg('comments__evaluation_value'))\
            .order_by('published_date')
    else:
        article_list = Article.objects\
            .filter(published_date__lte=timezone.now())\
            .filter(title__contains=request.GET.get('search'))\
            .annotate(avg_value=Avg('comments__evaluation_value'))\
            .order_by('published_date')
    paginator = Paginator(article_list, 10) #ページ表示数
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages) #ページが範囲外の時最終ページを表示する
    return render(request, 'news/article_list.html', {'articles':articles})

#評価順表示
def article_evaluationlist(request):
    #検索窓の内容の検知
    if request.GET.get('search') is None:
        article_list = Article.objects\
            .filter(published_date__lte=timezone.now())\
            .annotate(avg_value=Avg('comments__evaluation_value'))\
            .order_by('-avg_value')
    else:
        article_list = Article.objects\
            .filter(published_date__lte=timezone.now())\
            .filter(title__contains=request.GET.get('search'))\
            .annotate(avg_value=Avg('comments__evaluation_value'))\
            .order_by('-avg_value')
    paginator = Paginator(article_list, 10) #ページ表示数
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages) #ページが範囲外の時最終ページを表示する
    return render(request, 'news/article_list.html', {'articles':articles})

#記事の未公開リスト
@login_required
def article_draft_list(request):
    articles=Article.objects.filter(
        published_date__isnull=True
    ).filter(
        author=request.user
    ).order_by('created_date')
    return render(request, 'news/article_draft_list.html', {'articles': articles})


#－－－－－－－－記事－－－－－－－－－－

#記事の内容
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    #article.objects.order_by('-comments__created_date')
    return render(request, 'news/article_detail.html', {'article': article})


#記事新規投稿
@login_required
def article_new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'news/article_edit.html', {'form': form})


#記事編集
@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author != request.user:
        return redirect('article_detail', pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect(article_detail, pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'news/article_edit.html', {'form': form})


#Publishボタンが押された時のView
@login_required
def article_publish(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.publish()
    return redirect('article_detail', pk=pk)


#記事の削除
@login_required
def article_remove(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author == request.user:
        article.delete()
    return redirect('article_list')

#－－－－－－－－コメント－－－－－－－－－－
#コメント追加
def add_comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if int(request.POST['evaluation_value']) >= 0 and int(request.POST['evaluation_value']) <= 5:
            if form.is_valid:
                comment = form.save(commit=False)
                comment.article = article
                comment.save()
                return redirect('article_detail', pk=article.pk)
        else:
            form.errors['evaluation_value'] = '0~5の範囲で指定してください'
    else:
        form = CommentForm()
    
    return render(request, 'news/add_comment.html', {'form': form})

#コメント削除
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('article_detail', pk=comment.article.pk)

#新規登録
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('article_list')
    else:
        form = UserCreationForm()
    return render(request, 'news/signup.html', {'form': form})
