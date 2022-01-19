from django.shortcuts import render, redirect
from .forms import ProjectForm

# Create your views here.
def index(request):
    args = {}
    return render(request, 'translate_project/index.html', args)

def new_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('index')
    else:
        form = ProjectForm()
    args = {
        'form': form,
    }
    return render(request, 'translate_project/new_project.html', args)