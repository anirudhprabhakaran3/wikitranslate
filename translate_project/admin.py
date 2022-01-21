from django.contrib import admin
from .models import Project, Sentence, Translator

# Register your models here.
admin.site.register(Project)
admin.site.register(Sentence)
admin.site.register(Translator)