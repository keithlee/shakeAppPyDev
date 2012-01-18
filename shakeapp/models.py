from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

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

'''class UserProfile(models.Model):
	user = models.OneToOneField(User)
	recipeLikeList = models.CommaSeparatedIntegerField(max_length=200) 
	questionLikeList = models.CommaSeparatedIntegerField(max_length=200)
	
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)
	post_save.connect(create_user_profile, sender=User)'''
	
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
	