# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseServerError, Http404
from models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from random import randint
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import ast

def index(request):
	#itemList  = ["recipe","questions"]
	itemList = ['recipe','question']
	return render_to_response('shakeApp/index.html', {'itemList':itemList},
		context_instance=RequestContext(request))
# login
def loginUser(request):
	logout(request)
	error_msg = u"User is not authorized"
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('username') and post.has_key('password'):
			username = post['username']
			password = post['password']
			print "username ", username,"password", password
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request,user)					
					print "You provided a correct username and password"
					return HttpResponseRedirect(reverse('indexname'))
				else:
					print "Your account has been disabled"
			else:
				print "Your username and password were incorrect"
			error_msg = u"User does not have authorization"
	return HttpResponseServerError(error_msg)
	
def logoutUser(request):
	response = logout(request)
	return HttpResponseRedirect('/shakeApp/')


def recipeIndex(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shakeApp/')
	recipeList = Recipe.objects.all()
	recipe_id_list = []
	for recipe in recipeList:
		recipe_id_list.append(recipe.id)
	# Pass in array/Hash table of recipe_ids?
	recipeCount = Recipe.objects.count()
	return render_to_response('shakeApp/recipe/recipeIndex.html', 
		{ 'recipeList':recipeList, 'recipeCount':recipeCount,'recipe_id_list':recipe_id_list },
		context_instance=RequestContext(request))

def recipeDetail(request, recipe_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shakeApp/')
	p = get_object_or_404(Recipe, pk=recipe_id)
	return render_to_response('shakeApp/recipe/recipeDetail.html', {'recipe':p}, 
		context_instance=RequestContext(request))

def createRecipe(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shakeApp/')	
	error_msg = u"Please input a name and text for your recipe"
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('name') and post.has_key('text'):
			name=post['name']
			text=post['text']
			# Check if recipe data is empty
			if not( name.isspace() or name=="" or text.isspace() or text=="" ):
				name = post['name']
				if Recipe.objects.filter(name=name).count() > 0:
					error_msg = u"Recipe name already created."
				else:
					text = post['text']
					newRecipe = Recipe.objects.create(name=name,text=text)
					return HttpResponseRedirect('/shakeApp/recipe/')
	return HttpResponseServerError(error_msg)

def likeRecipe(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shakeApp/')
	post = request.POST.copy()
	recipeName = post['recipe_name']
	user = request.user
	username = user.username
	
	if RecipeLikes.objects.filter(username=username,recipeName=recipeName).count() >0:
		return HttpResponseServerError("You already liked this Recipe. Now cook it!")
	#Create Likes table that keeps track of recipes that the users have liked. 
	RecipeLikes.objects.create(user=User.objects.get(username=username), recipe=Recipe.objects.get(name=recipeName), 
						username=username, recipeName=recipeName)
	qset = Recipe.objects.filter(name=recipeName)
	recipe = qset[0]
	recipe.numLikes = recipe.numLikes + 1
	recipe.save()
	return HttpResponseRedirect('/shakeApp/recipe/')
	
def deleteRecipe(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shakeApp/')
	post = request.POST.copy()
	user = request.user
	recipeName = post['recipe_name']
	Recipe.objects.filter(name=recipeName).delete()
	RecipeLikes.objects.filter(username=user.username, recipeName=recipeName).delete()
	return HttpResponseRedirect('/shakeApp/recipe/')

def randomRecipe(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shakeApp/')	
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('ingredient'):
			ingredient = post['ingredient']
			q = Recipe.objects.filter(text__icontains=ingredient)
			# Ingredient is in atleast one recipe added.
			if q.count() > 0:
				randomNum = randint(0, q.count()-1)
				p = q[randomNum]
				return render_to_response('shakeApp/recipe/recipeDetail.html', {'recipe':p}, 
					context_instance=RequestContext(request))
			else:
				return HttpResponseNotFound('<h1>Sorry no recipe uses %s as an ingredient' % ingredient)
		else:
			allRecipes = Recipe.objects.all()
			randomNum = randint(0, allRecipes.count()-1)
			p = allRecipes[randomNum]
			return render_to_response('shakeApp/recipe/recipeDetail.html', {'recipe':p}, 
					context_instance=RequestContext(request))

# Questions 

def questionIndex(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shakeApp/')
	questionList = Question.objects.all()
	question_id_list = []
	for question in questionList:
		question_id_list.append(question.id)
	# Pass in array/Hash table of recipe_ids?
	questionCount = Question.objects.count()
	return render_to_response('shakeApp/question/questionIndex.html', 
		{ 'questionList':questionList, 'questionCount':questionCount,'question_id_list':question_id_list },
		context_instance=RequestContext(request))
	
def questionDetail(request, question_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shakeApp/')
	p = get_object_or_404(Question, pk=question_id)
	return render_to_response('shakeApp/question/questionDetail.html', {'question':p}, 
		context_instance=RequestContext(request))
		
def createQuestion(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shakeApp/')	
	error_msg = u"Please input a name and text for your question"
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('name') and post.has_key('text'):
			name = post['name']
			text = post['text']
			# Check if data is empty
			if not(name.isspace() or name=="" or text.isspace() or text==""):
				if Question.objects.filter(name=name).count() > 0:
					error_msg = u"Question name already created."
				else:
					text = post['text']
					newQuestion = Question.objects.create(name=name,text=text)
					return HttpResponseRedirect('/shakeApp/question/')
	return HttpResponseServerError(error_msg)

def likeQuestion(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shakeApp/')
	post = request.POST.copy()
	questionName = post['question_name']
	user = request.user
	username = user.username
	
	if QuestionLikes.objects.filter(username=username,questionName=questionName).count() >0:
		return HttpResponseServerError("You already liked this Question. Now add another question! :)")
	#Create Likes table that keeps track of recipes that the users have liked. 
	QuestionLikes.objects.create(user=User.objects.get(username=username), question=Question.objects.get(name=questionName), 
						username=username, questionName=questionName)
	qset = Question.objects.filter(name=questionName)
	question = qset[0]
	question.numLikes = question.numLikes + 1
	question.save()
	return HttpResponseRedirect('/shakeApp/question/')

def deleteQuestion(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shakeApp/')	
	post = request.POST.copy()
	user = request.user
	questionName = post['question_name']
	Question.objects.filter(name=questionName).delete()
	QuestionLikes.objects.filter(username= user.username, questionName=questionName).delete()
	return HttpResponseRedirect('/shakeApp/question/')

def randomQuestion(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/shakeApp/')	
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('keyword'):
			keyword = post['keyword']
			q = Question.objects.filter(text__icontains=keyword)
			# Ingredient is in atleast one recipe added.
			if q.count() > 0:
				randomNum = randint(0, q.count()-1)
				p = q[randomNum]
				return render_to_response('shakeApp/question/questionDetail.html', {'question':p}, 
					context_instance=RequestContext(request))
			else:
				return HttpResponseNotFound('<h1>Sorry no question with %s has been added yet' % keyword)
		else:
			allQuestions = Question.objects.all()
			randomNum = randint(0, allQuestions.count()-1)
			p = allQuestions[randomNum]
			return render_to_response('shakeApp/question/questionDetail.html', {'question':p}, 
					context_instance=RequestContext(request))
























