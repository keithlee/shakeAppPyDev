from models import Recipe, Question
from dbindexer.api import register_index

register_index(Recipe, {'text': 'icontains'})