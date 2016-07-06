from django.utils.six.moves.urllib.parse import (
    quote, quote_plus, unquote, unquote_plus, urlencode as original_urlencode,
    urlparse,
)
from django.http import Http404
from gym.models import Post
from rest_framework.response import Response
from django.contrib import messages
from .forms import PostForm
from django.http import HttpResponse , HttpResponseRedirect 
from django.shortcuts import render ,get_object_or_404 ,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def post_create(request):
	# if not request.user.is_staff or not request.user.is_superuser:
	# 	raise Http404("No tiene acceso para esta función")
	# if not request.user.is_authenticated():
	# 	raise Http404("No tiene acceso para esta función")
	form = PostForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.publish = form.cleaned_data['publish']
		instance.save()
		#MESSENGES SUCCESS
		messages.success(request, "Successfuly create")
		return HttpResponseRedirect(instance.get_absolute_url())

	# else:
	# 	messages.success(request, "Not Successfuly create")
	context = {
		"form" : form,
	}
	return render(request,"post_form.html",context)

def post_detail(request, slug=None):

	instance = get_object_or_404(Post, slug=slug)
	share_string = quote_plus(instance.content)
	context ={
		"title": instance.title,
		"instance": instance,
	}
	return render(request,"post_detail.html",context)

def post_list(request):
	queryset_list = Post.objects.all()
	#Cambiar la numeracion si se quiere visualizar menos post
	query = request.GET.get("query")
	if query:
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(content__icontains=query)).distinct()
	paginator = Paginator(queryset_list,25)
	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)
	context ={
			"object_list": queryset,
			"title":"My user list"
		}

	return render(request,"index.html",context)



def post_update(request,id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404("No tiene acceso para esta función")
	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, request.FILES or None,instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		#MESSENGES SUCCESS
		messages.success(request, "Item save")
		return HttpResponseRedirect(instance.get_absolute_url())
	# else:
	# 	messages.error(request, "Item not save")
	context ={
		"title": instance.title,
		"instance": instance,
		"form" : form
	}
	return render(request,"post_form.html",context)

def post_delete(request,id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404("No tiene acceso para esta función")
	instance = get_object_or_404(Post,id=id)
	instance.delete()
	messages.success(request, "Successfuly delete")
	return redirect("post:list") 
	 

