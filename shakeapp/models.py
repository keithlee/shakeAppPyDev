__author__ = "Keith Lee"
__email__ = "keithlee002@gmail.com"

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
	name = models.CharField(max_length=200)
	text = models.TextField(blank=True, null=True)
	numLikes = models.IntegerField(default=0)
	def __unicode__(self):
		return u"Recipe(%s, %s, %d)" % (self.name, self.text,self.numLikes)

class Question(models.Model):
	name = models.CharField(max_length=200)
	text = models.TextField(blank=True, null=True)
	numLikes = models.IntegerField(default = 0)
	def __unicode__(self):
		return u"Question(%s, %s, %d)" % (self.name, self.text, self.numLikes)
	
class RecipeLikes(models.Model):
	user = models.ForeignKey(User) 
	recipe = models.ForeignKey('Recipe')
	username= models.CharField(max_length=200)
	recipeName = models.CharField(max_length=200)
	def __unicode__(self):
		return u"likes(%s, %s, %s, %s)" % (self.user, self.recipe, self.username, self.recipeName)
	
class QuestionLikes(models.Model):
	user = models.ForeignKey(User) 
	question = models.ForeignKey('Question')
	username= models.CharField(max_length=200)
	questionName = models.CharField(max_length=200)
	def __unicode__(self):
		return u"likes(%s, %s, %s, %s)" % (self.user, self.question, self.username, self.questionName)
	