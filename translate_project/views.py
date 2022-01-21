from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Project, Sentence
from .forms import ProjectForm
from .services import get_sentences_from_title, does_wiki_exist

# Create your views here.
def index(request):
    args = {}
    return render(request, 'translate_project/index.html', args)

def dashboard(request):
    projects = Project.objects.all()
    projects_count = projects.count()
    sentences_count = Sentence.objects.count()
    args = {
        'projects': projects,
        'projects_count': projects_count,
        'sentences_count': sentences_count,
    }
    return render(request, 'translate_project/dashboard.html', args)

def view_project(request, project_pk):
    project = Project.objects.get(pk=project_pk)
    sentences = Sentence.objects.filter(project=project)
    args = {
        'project' : project,
        'sentences': sentences,
    }
    return render(request, 'translate_project/view_project.html', args)

def new_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if does_wiki_exist(form['wiki_title'].value()):
            if form.is_valid():
                project = form.save(commit=False)
                project.save()
                generate_sentences(project)
                return redirect('dashboard')
        else:
            messages.add_message(request, messages.ERROR, 'Error: Invalid Page.')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = ProjectForm()
    args = {
        'form': form,
    }
    return render(request, 'translate_project/new_project.html', args)

def translate(request, project_pk):
    project = Project.objects.get(pk=project_pk)
    sentences = Sentence.objects.filter(project=project)
    args = {
        'project': project,
        'sentences': sentences,
    }
    return render(request, 'translate_project/translate.html', args)

def submit_translation(request):
    if is_ajax(request) and request.method == 'POST':
        sentence_id = request.POST.get('sentence_id')
        translated_sentence = request.POST.get('translated_sentence')
        sentence = Sentence.objects.get(pk=sentence_id)
        sentence.translated_sentence = translated_sentence
        sentence.save()
        return JsonResponse({'status': 'success'})


def generate_sentences(project):
    sentences = get_sentences_from_title(project.wiki_title)
    for sentence in sentences:
        s = Sentence(project=project, original_sentence=sentence)
        s.save()

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'