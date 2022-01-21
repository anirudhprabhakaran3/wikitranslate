from dataclasses import field
from django import forms
from .models import Project, Translator

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('wiki_title', 'target_language')

class AssignTranslatorForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('appointed_translator',)

class ChangePermissionsTranslator(forms.ModelForm):
    class Meta:
        model = Translator
        fields = ('is_manager',)