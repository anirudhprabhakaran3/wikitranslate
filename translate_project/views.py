from click import password_option
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Project, Sentence, Translator
from .forms import ProjectForm, AssignTranslatorForm, ChangePermissionsTranslator
from .services import get_sentences_from_title, does_wiki_exist

# Create your views here.
def index(request):
    args = {}
    return render(request, 'translate_project/index.html', args)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            create_translator(user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    args = {
        'form': form,
    }
    return render(request, 'registration/signup.html', args)

@login_required
def dashboard(request):
    translator = Translator.objects.get(user=request.user)
    if translator.is_manager:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(appointed_translator=translator)
    projects_count = projects.count()
    sentences_count = Sentence.objects.filter(project__in=projects).count()
    args = {
        'projects': projects,
        'projects_count': projects_count,
        'sentences_count': sentences_count,
    }
    return render(request, 'translate_project/dashboard.html', args)

@login_required
def view_project(request, project_pk):
    project = Project.objects.get(pk=project_pk)
    sentences = Sentence.objects.filter(project=project)
    args = {
        'project' : project,
        'sentences': sentences,
    }
    return render(request, 'translate_project/view_project.html', args)

@login_required
def new_project(request):
    require_manager(request)
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

@login_required
def translate(request, project_pk):
    project = Project.objects.get(pk=project_pk)
    sentences = Sentence.objects.filter(project=project)
    args = {
        'project': project,
        'sentences': sentences,
    }
    return render(request, 'translate_project/translate.html', args)

@login_required
def submit_translation(request):
    if is_ajax(request) and request.method == 'POST':
        sentence_id = request.POST.get('sentence_id')
        translated_sentence = request.POST.get('translated_sentence')
        sentence = Sentence.objects.get(pk=sentence_id)
        sentence.translated_sentence = translated_sentence
        sentence.save()
        return JsonResponse({'status': 'success'})

@login_required
def admin_page(request):
    require_manager(request)
    translators = Translator.objects.count()
    projects = Project.objects.count()
    sentences = Sentence.objects.count()
    args = {
        'translators': translators,
        'projects': projects,
        'sentences': sentences,
    }
    return render(request, 'translate_project/admin_page.html', args)

@login_required
def admin_projects(request):
    require_manager(request)
    projects = Project.objects.all()
    args = {
        'projects': projects,
    }
    return render(request, 'translate_project/admin_projects.html', args)

@login_required
def assign_translator(request, project_pk):
    require_manager(request)
    project = Project.objects.get(pk=project_pk)
    if request.method == 'POST':
        form = AssignTranslatorForm(request.POST)
        if form.is_valid():
            project.appointed_translator = form.cleaned_data.get('appointed_translator')
            project.save()
            messages.add_message(request, messages.SUCCESS, 'Translator assigned/modified.')
            return redirect('admin_projects')
    else:
        form = AssignTranslatorForm(instance=project)
    args = {
        'project': project,
        'form': form,
    }
    return render(request, 'translate_project/assign_translator.html', args)

@login_required
def admin_translators(request):
    require_manager(request)
    translators = Translator.objects.all()
    args = {
        'translators': translators,
    }
    return render(request, 'translate_project/admin_translators.html', args)

@login_required
def change_permissions(request, translator_pk):
    require_manager(request)
    translator = Translator.objects.get(pk=translator_pk)

    if request.user == translator.user:
        messages.add_message(request, messages.ERROR, 'Error: You cannot change your own permissions.')
        return redirect('admin_translators')

    if request.method == 'POST':
        form = ChangePermissionsTranslator(request.POST)
        if form.is_valid():
            translator.is_manager = form.cleaned_data.get('is_manager')
            translator.save()
            messages.add_message(request, messages.SUCCESS, 'Permissions changed.')
            return redirect('admin_translators')
    else:
        form = ChangePermissionsTranslator(instance=translator)
    args = {
        'translator': translator,
        'form': form,
    }
    return render(request, 'translate_project/change_permissions.html', args)

## Helper Functions

def generate_sentences(project):
    sentences = get_sentences_from_title(project.wiki_title)
    for sentence in sentences:
        s = Sentence(project=project, original_sentence=sentence)
        s.save()

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def create_translator(user):
    translator = Translator(user=user, is_manager=False)
    translator.save()

def require_manager(request):
    translator = Translator.objects.get(user=request.user)
    if not translator.is_manager:
        messages.add_message(request, messages.ERROR, 'You are not authorized to create a project.')
        return redirect('dashboard')