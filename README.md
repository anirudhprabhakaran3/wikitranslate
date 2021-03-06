# WikiTranslate

<img src="https://img.shields.io/github/license/anirudhprabhakaran3/wikitranslate"><img src="https://img.shields.io/github/languages/top/anirudhprabhakaran3/wikitranslate"><img src="https://img.shields.io/github/languages/code-size/anirudhprabhakaran3/wikitranslate"><img src="https://img.shields.io/github/issues/anirudhprabhakaran3/wikitranslate"><img src="https://img.shields.io/github/issues-pr/anirudhprabhakaran3/wikitranslate"><img src="https://img.shields.io/github/last-commit/anirudhprabhakaran3/wikitranslate">


Welcome to WikiTranslate! This is a web portal where you can enter the name of a Wikipedia page. The service will download the summary of the page, and you can translate the sentences into the language you are familiar with.

Supported languages: 
- Bengali
- Gujarati
- Hindi (hi)
- Kannada
- Malayalam
- Marathi
- Nepali
- Oriya
- Panjabi
- Sinhala
- Tamil
- Telugu
- Urdu

## Installation
To contribute and work on the repository, you need Python installed on your system. If you do not have Python installed, you can install it from [here](https://www.python.org/downloads/).

Fork and clone the repository from GitHub.

```bash
git clone https://github.com/<your-username-here>/wikitranslate.git
# If you want to use SSH
git clone git@github.com:<your-username-here>/wikitranslate.git

# Move to the directory
cd wikitranslate
```

I would recommend you to create a virtual environment and install the dependencies.

```bash
python3 -m venv <name-of-virtual-environment>
source <name-of-virtual-environment>/bin/activate

# Install the dependencies
pip install -r requirements.txt
```

Create the migrations so that you can set up the database.
```bash
python manage.py migrate
```

After the migration is completed, create a superuser, and run the server!
```bash
# Create superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

The server is now running. You can now access the application at  `http://localhost:8000`

## Models

There are three models in the application - `Translator`, `Project` and `Sentence`.

`Translator` is the model for each individual. It contains
- `user`: A One-To-One relationship with Django's `User` model.
- `is_manager`: A boolean field which keeps track of whether a particular translator is a manager or not.

`Project` is the model for each project. It contains
- `id`: Unique id of the project
- `wiki_title`: Title of the Wikipedia page
- `target_language`: Target language of the translation project
- `appointed_translator`: Foreign key to the translator who is appointed to the project

`Sentence` is the model for every translated sentence. It contains
- `id`: Unique id of the sentence
- `project`: The associated project for the sentence
- `original_sentence`: The original sentence
- `translated_sentence`: The translated sentence

## Implementation

In my implementation, I leverage the Django Authentication System. Since I didn't have to store lots of data, I didn't extend `AbstractUser`, but instead, created `Translator`, which has a One-To-One relationship with `User`.

Also, I have designed my app in a way in which a particular translator can only be alloted a single project at a time. Once a project is complete, the translator can be removed from that, and work on another project.

## Tech
The project is made using the Django framework based on Python.

I have used SQLite for the database, as there is no need for a production ready database for a demo project.

For the frontend, I am using Bootstrap 5. The forms are rendered using Crispy Forms, using the Bootstrap framework. Tables are rendered using DataTables, a jQuery plugin.

I am leveraging the Messages service to display messages to the user. I am using AJAX to send the AJAX request to the server to update the translated sentences.