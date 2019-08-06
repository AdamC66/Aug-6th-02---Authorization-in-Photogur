from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from photogur.models import Picture, Comment
from django.db.models import Q
from photogur.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def root(request):
    return HttpResponseRedirect('pictures')

def pictures(request):
    context = {'pictures': Picture.objects.all()}
    response = render(request, 'pictures.html', context)
    return HttpResponse(response)

def picture_show(request, id):
    picture = Picture.objects.get(pk=id)
    context = {'picture':picture}
    return render(request, 'picture.html', context)

def picture_search(request):
    query = request.GET['query']
    search_results = Picture.objects.filter(Q(artist__icontains=query) | Q(title__icontains=query))
    context = {'pictures': search_results, 'query':query}
    return render(request, 'search.html', context)

def create_comment(request):
    picture_id = request.POST['picture']
    picture = Picture.objects.filter(id=picture_id).first()
    name = request.POST['name']
    message = request.POST['message']
    new_comment = Comment(name=name, message=message, picture = picture)
    new_comment.save()
    context = {'picture':picture}
    return render(request,'picture.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/pictures')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    context = {'form': form}
    http_response = render(request, 'login.html', context)
    return HttpResponse(http_response)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/pictures')

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/pictures')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/pictures')
    else:
        form = UserCreationForm()
    html_response =  render(request, 'signup.html', {'form': form})
    return HttpResponse(html_response)

@login_required
def submit(request):
    if request.method == 'POST':
        new_picture = Picture(title = request.POST['title'], artist = request.POST['artist'], url = request.POST['url'], user = request.user)
        new_picture.save()
        context = {'picture': new_picture}
        return render(request,'picture.html', context)
    else:
        return render(request, 'submit.html')

@login_required
def edit(request, id):
    picture = get_object_or_404(Picture, pk=id, user=request.user.pk)
    if request.method == 'POST':
        picture.title = request.POST['title']
        picture.artist = request.POST['artist']
        picture.url = request.POST['url']
        picture.save()
        context = {'picture':picture}
        return render(request,'picture.html', context)
    else:
        context = {'picture':picture}
        return render(request, 'edit.html', context)