from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('shakeapp.views',
    # Examples:
    
	#url(r'^shakeApp/', 'shakeApp.views.index'),
	 url(r'^$', 'index', name= 'indexname'),
	 url(r'^shakeApp/$', 'index', name= 'indexname'),
	 
	 url(r'^shakeApp/recipe/$', 'recipeIndex'),
	 url(r'^shakeApp/recipe/(?P<recipe_id>\d+)/$', 'recipeDetail'),
	 url(r'^shakeApp/recipe/create/$','createRecipe'),
	 url(r'^shakeApp/recipe/delete/$','deleteRecipe'),
     url(r'^shakeApp/recipe/like/$','likeRecipe'),
	 url(r'^shakeApp/recipe/random/$','randomRecipe'),
	 
	 url(r'^shakeApp/logout/$', 'logoutUser'),
	 
	 url(r'^shakeApp/question/$', 'questionIndex'),
	 url(r'^shakeApp/question/(?P<question_id>\d+)/$', 'questionDetail'),
	 url(r'^shakeApp/question/create/$','createQuestion'),
	 url(r'^shakeApp/question/delete/$','deleteQuestion'),
     url(r'^shakeApp/question/like/$','likeQuestion'),     
	 url(r'^shakeApp/question/random/$','randomQuestion'),

	 )
urlpatterns += patterns('',
	url(r'^shakeApp/login/$', 'django.contrib.auth.views.login'),
	url('^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^admin/', include(admin.site.urls)),

	)
    # url(r'^webProjects/', include('webProjects.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
