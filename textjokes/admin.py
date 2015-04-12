from django.contrib import admin
from models import TextJokeCategory, TextJoke, TextPunchline, JokeVotes, \
    TextComment

admin.site.register(TextJokeCategory)
admin.site.register(TextJoke)
admin.site.register(TextPunchline)
admin.site.register(JokeVotes)
admin.site.register(TextComment)