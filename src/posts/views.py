""" Render, httpresponse, getobjector404... """
from django.http import HttpResponseRedirect, Http404 #, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostForm


# Create your views here.
def post_create(request):
    """ Create Post """
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    # request.FILES has to be defined when file upload in Form
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Post succesfully added')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, 'Cannot create post')

    context = {
        'form': form,
    }
    return render(request, 'post_form.html', context)

def post_detail(request, post_slug=None):
    """ Post Detail """
    # instance = Post.objects.get('id=2')
    instance = get_object_or_404(Post, slug=post_slug)
    context = {
        'title': instance.title,
        'instance': instance,
    }
    return render(request, 'post_detail.html', context)

def post_list(request):
    """ List all Posts """
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 5) # Show 10 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'post_list.html', {'posts': posts})

def post_update(request, post_slug):
    """ Update Post """
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, slug=post_slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get("title"))
        instance.save()
        messages.success(request, 'Post succesfully updated')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, 'Cannot create post')

    context = {
        'title': instance.title,
        'instance': instance,
        'form': form,
    }
    return render(request, 'post_form.html', context)

def post_delete(request, post_slug):
    """ Delete Post """
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, slug=post_slug)
    instance.delete()
    return redirect('posts:list')
