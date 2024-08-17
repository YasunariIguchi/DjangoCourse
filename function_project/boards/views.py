from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Theme, Comment
from django.http import Http404
from django.core.cache import cache
from django.http import JsonResponse

# Create your views here.
@login_required
def create_theme(request):
    create_theme_form = forms.CreateThemeForm(request.POST or None)
    if create_theme_form.is_valid():
        create_theme_form.instance.user = request.user
        create_theme_form.save()
        # theme = create_theme_form.save(commit=False)
        # theme.user = request.user
        # theme.save()
        messages.success(request, "テーマを作成したお")
        return redirect("boards:list_themes")
    return render(request, "boards/create_theme.html", context={
        "create_theme_form": create_theme_form,
    })

def list_themes(request):
    data = Theme.objects.fetch_all_themes()
    return render(request, "boards/list_themes.html", context={
        "data": data,
    })

def edit_theme(request, id):
    theme = get_object_or_404(Theme, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    form = forms.EditThemeForm(request.POST or None, instance=theme)
    if form.is_valid():
        form.save()
        messages.success(request, "タイトルを更新しました。")
        return redirect("boards:list_themes")
    return render(request, "boards/edit_theme.html", context={
        "form": form,
        "id": id,
    })

def delete_theme(request, id):
    theme = get_object_or_404(Theme, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    if request.method =="POST":
        theme.delete()
        messages.success(request, "掲示板を削除しました。")
        return redirect("boards:list_themes")
    return render(request, "boards/delete_theme.html", context={
        "id": id,
        "title": theme.title
    })

def post_comment(request, theme_id):
    saved_comment = cache.get(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', "")
    form = forms.PostCommentForm(request.POST or None, initial={"comment": saved_comment})
    comments = Comment.objects.fetch_by_theme_id(theme_id)
    if form.is_valid():
        if not request.user.is_authenticated:
            raise Http404
        form.instance.user = request.user
        form.instance.theme = get_object_or_404(Theme, id=theme_id)
        form.save()
        cache.delete(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}')
        messages.success(request, "コメントを投稿しました。")
        return redirect("boards:list_themes")
    return render(request, "boards/post_comment.html", context={
        "form": form,
        "theme_id": theme_id,
        "comments": comments
    })

def save_comment(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        comment = request.GET.get("comment")
        theme_id = request.GET.get("theme_id")
        if comment and theme_id:
            cache.set(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', comment)
            return JsonResponse({"message": "一時保存しました"})
    return JsonResponse({"message": "無効なリクエストです"}, status=400)

