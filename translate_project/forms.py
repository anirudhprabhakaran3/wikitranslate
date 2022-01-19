from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('wiki_title', 'target_language')