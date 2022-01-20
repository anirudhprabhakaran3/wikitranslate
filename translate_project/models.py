from django.db import models

# Create your models here.

class Project(models.Model):

    # Languages
    BENGALI = 'bn'
    GUJARATI = 'gu'
    HINDI = 'hi'
    KANNADA = 'kn'
    MALAYALAM = 'ml'
    MARATHI = 'mr'
    NEPALI = 'ne'
    ORIYA = 'or'
    PUNJABI = 'pa'
    SINHALA = 'si'
    TAMIL = 'ta'
    TELUGU = 'te'
    URDU = 'ur'

    LANGUAGE_CHOICES = (
        (BENGALI, 'Bengali'),
        (GUJARATI, 'Gujarati'),
        (HINDI, 'Hindi'),
        (KANNADA, 'Kannada'),
        (MALAYALAM, 'Malayalam'),
        (MARATHI, 'Marathi'),
        (NEPALI, 'Nepali'),
        (ORIYA, 'Oriya'),
        (PUNJABI, 'Punjabi'),
        (SINHALA, 'Sinhala'),
        (TAMIL, 'Tamil'),
        (TELUGU, 'Telugu'),
        (URDU, 'Urdu'),
    )

    wiki_title = models.CharField(max_length=200)
    target_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)

    def __str__(self):
        return self.wiki_title

class Sentence(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    original_sentence = models.TextField()
    translated_sentence = models.TextField()

    def __str__(self):
        return self.original_sentence