""" Render, httpresponse, getobjector404... """
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Post
from .forms import PostForm


# Create your views here.
def post_create(request):
    """ Create Post """
    form = PostForm(request.POST or None)
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

def post_detail(request, post_id=None):
    """ Post Detail """
    # instance = Post.objects.get('id=2')
    instance = get_object_or_404(Post, id=post_id)
    context = {
        'title': instance.title,
        'instance': instance
    }
    return render(request, 'post_detail.html', context)

def post_list(request):
    """ List all Posts """
    queryset = Post.objects.all()
    context = {
        'title': 'My user list',
        'object_list': queryset
    }

    return render(request, 'post_list.html', context)


    # if request.user.is_authenticated():
    #     context = {
    #         'title': 'My user list'
    #     }
    # else:
    #     context = {
    #         'title': 'List'
    #     }


    # return render(request, "index.html", context)

def post_update(request, post_id):
    """ Update Post """
    instance = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=instance)
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

def post_delete(request, post_id):
    """ Delete Post """
    instance = get_object_or_404(Post, id=post_id)
    instance.delete()
    return redirect('posts:list')
