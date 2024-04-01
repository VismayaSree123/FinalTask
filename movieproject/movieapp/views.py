from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.template.defaultfilters import slugify

from . forms import movieform
from . models import Category,Movie
from django.core.paginator import Paginator,EmptyPage,InvalidPage

# Create your views here.

def allMovieCat(request,c_slug=None):
    c_page=None
    movie_list=None
    if c_slug!=None:
        c_page=get_object_or_404(Category,slug=c_slug)
        movie_list=Movie.objects.all().filter(category=c_page)
    else:
        movie_list=Movie.objects.all().filter()
    paginator=Paginator(movie_list,6)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        movies=paginator.page(page)
    except(EmptyPage,InvalidPage):
        movies=paginator.page(paginator.num_pages)
    return render(request,'category.html',{'category':c_page,'movies':movies})

def movieDetail(request,c_slug,p_slug):
    try:
        movie=Movie.objects.get(category__slug=c_slug,slug=p_slug)
    except Exception as e:
        raise e
    return  render(request,'movie.html',{"movie":movie})
def addMovie(request):
    if request.method=='POST':
        name1=request.POST.get('name')
        desc1=request.POST.get('desc')
        rel_date1=request.POST.get('rel_date')
        img1=request.FILES['img']
        cast1=request.POST.get('cast')
        trailer1=request.POST.get('trailer')
        genre1=request.POST.get('genre')
        genre2=Category.objects.get(name=genre1)
        slug=slugify(name1)
        mv=Movie(name=name1,desc=desc1,image=img1,rel_date=rel_date1,cast=cast1,trailer=trailer1,category=genre2,uid=request.user,slug=slug)
        mv.save()
        return redirect('/movieapp')
    else:
        return render(request,'add.html')

def updateMovie(request,id):
    mv3=get_object_or_404(Movie,id=id)
    if request.method=='POST':
        fm=movieform(request.POST,instance=mv3)
        if fm.is_valid():
            fm.save()
            return redirect('/movieapp')
    else:
        fm=movieform(instance=mv3)

    return render(request,'edit.html',{'fm':fm,'mv3':mv3})


def myMovies(request):
    movies=Movie.objects.filter(uid=request.user.id)
    return render(request,'mymovies.html',{'movies':movies})


def deleteMovie(request,id):
    if request.method=='POST':
        mv4=Movie.objects.get(id=id)
        mv4.delete()
        return redirect('/movieapp/mymovies')
    return render(request,'delete.html')