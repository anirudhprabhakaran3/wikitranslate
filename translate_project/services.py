from wikipediaapi import Wikipedia
import nltk

def get_sentences_from_title(wiki_title):
    intro = Wikipedia().page(wiki_title).summary
    intro_sentences = nltk.sent_tokenize(intro)
    return intro_sentences