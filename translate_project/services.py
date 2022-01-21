from wikipediaapi import Wikipedia
import nltk

def does_wiki_exist(title):
    nltk.download('punkt')
    wiki_wiki = Wikipedia('en')
    return wiki_wiki.page(title).exists()

def get_sentences_from_title(wiki_title):
    wiki_wiki = Wikipedia('en')
    intro = wiki_wiki.page(wiki_title).summary        
    intro_sentences = nltk.sent_tokenize(intro)
    return intro_sentences