from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import forms
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from xml.etree import ElementTree
import datetime
import hashlib
import os

from videoRepository.models import	Person, Video
from videoRepository.forms import LoginForm, NewUserForm
from test3 import settings


################################################## Custom Exceptions: ##################################################
class NotXMLException(Exception):
    """Custom exception for when the user submits a manifest that is not XML."""
    pass

######################################################## Views: ######################################################## 
class VRIndex(generic.View):
	""" This is the view for the index of the video repository.  It handles two forms: LoginForm and NewUserForm.
		If the user submits login info, the post method will validate that info, log the user in and redirect to
		their video repository.  If the user submits new user info, the post method will validate that info and 
		create a new user.  The index is rendered with a message that the account creation succeeded.  Any errors
		along the way (e.g. bad login, etc.) are handled by rendering the index with a message.

		There are a number of ways that this site redirects back to the index.  If a user is logged on, the GET
		method will automatically redirect to the user's video repository.  If no user is logged on, the GET method
		will render a blank index page.
	"""
	def get(self, request):
		if request.user.is_authenticated():
			# Redirect logged on user to their repository right away
			return HttpResponseRedirect('UserRepository/{0:s}'.format(request.user.username))
		else:
			loginForm = LoginForm() # An unbound form
			newUserForm = NewUserForm()
			return render(	request,
							'videoRepository/index.html',
							{'loginForm':loginForm, 'newUserForm':newUserForm, 'serverMessage':'You are not logged in at this time.'}	)

	def post(self, request):

		loginForm = LoginForm(request.POST) # A form bound to the POST data
		newUserForm = NewUserForm(request.POST) # A form bound to the POST data
		serverMessage = ''
		#import pdb; pdb.set_trace()

		# All validation rules pass for the LoginForm
		if loginForm.is_valid():
			# Process the data in form.cleaned_data
			username = loginForm.cleaned_data['loginusername']
			password = loginForm.cleaned_data['loginpassword']
			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					login(request, user)
					try:
						person = Person.objects.get(user__username=username)
					except:
						serverMessage = "Database error retrieving video repository for '{0:s}'.".format(username)
					else:
						return HttpResponseRedirect('UserRepository/{0:s}'.format(username)) # Redirect after POST
				else:
					serverMessage = "Account is disabled for user '{0:s}'.  Please contact the site administrator.".format(username)
			else:
				serverMessage = "Invalid login for user '{0:s}'.  Please contact the site administrator.".format(username)

		# Check for new user submission.  If valid, add user and redirect to their (empty) repository page.
		elif newUserForm.is_valid():
			# Process the data in form.cleaned_data
			firstname = newUserForm.cleaned_data['newfirstname']
			lastname = newUserForm.cleaned_data['newlastname']
			username = newUserForm.cleaned_data['newusername']
			password = newUserForm.cleaned_data['newpassword']

			try:
				user = User.objects.create_user(username, '', password)
			except:
				serverMessage = "Unable to create a new user account for '{0:s}'.  Please contact the site administrator.".format(username)
			else:
				user.first_name = firstname
				user.last_name = lastname
				user.save()
				person = Person(user=user)
				person.save()
				mediapath = os.path.join(settings.MEDIA_ROOT, username)
				if not os.path.exists(mediapath):
					os.mkdir(mediapath)
				serverMessage = "New account created for '{0:s}.".format(username)

		# If the LoginForm validates, it will redirect to the user repository page.  In all other cases, we are going to render an unbound
		# form on the index page.  In each case, we create a server message that is appropriate for the reason we are rendering the index page.
		loginForm = LoginForm()
		newUserForm = NewUserForm()
		return render(request, 'videoRepository/index.html', {'loginForm':loginForm, 'newUserForm':newUserForm, 'serverMessage':serverMessage})

class UserRepository(generic.ListView):
	""" This is the view that renders the user's repository.  It will only render a repository specifically for an authenticated
		user.  For example, if 'tom' is logged on and tries to manually enter the url a different repository, 'tom' will ge
		redirected to the index.  Similarly, if someone else manually enters a url for a user that does not exist, the view
		redirects to the index.  But if the user is a member of the 'staff' group, that user can view any extant repository.

		This is a list view that returns a query set.  The query set has two master indeces with each containing a list.
		Index zero contains the a list where the first element is the user's full name, the second element is who is logged
		on at the time (it can be different when 'staff' is viewing the page) and the third element is the username who's 
		repository is being viewed.
		Index one contains a list of elements, each of which contains the data for a video the user has uploaded.
	"""
	template_name = 'videoRepository/userRepository.html'
	context_object_name = 'videoList'
	allow_empty = False 				# Causes 404 to be raised if queryset is empty
	
	def get(self, request, *args, **kwargs):
		# Ideally, we would prefer to use in built-in authentication such as @method_decorator(user_passes_test(checkUser, login_url='/')),
		# but it isn't obvious how to do this using class-based views.  The problem is the decorator method only sees which user is logged in,
		# if any, but it doesn't know which page has been requested.  We don't want users seeing each other's pages.  So, for now, we will
		# write our own method.  In this case, the 'username' is a parameter passed from urls.py, so that is the page requested.  We can use
		# that parameter to make sure that that user is logged in.
		#import pdb; pdb.set_trace()
		if(request.user.is_authenticated() and (request.user.username == kwargs['username'] or request.user.is_staff)):
			try:
				return super(UserRepository, self).get(request, *args, **kwargs)
			except Http404:
				return HttpResponseRedirect('/')
		else:
				return HttpResponseRedirect('/')

	def get_queryset(self):
		#import pdb; pdb.set_trace()
		videoList = []
		try:
			person = Person.objects.get(user__username=self.kwargs['username'])
		except:
			pass	# Empty list will raise 404 in the get() method
		else:
			fullName = '{0:s} {1:s}'.format(person.user.first_name, person.user.last_name)
			videoList.append((fullName, self.request.user.username, person.user.username))

			# In a real-world application, we would stand up a media server or at least a location on the same server.
			# In this case, to keep it simple, we are modifying the location based on a field we created in settings.py.
			videoSet = person.video_set.all()
			for video in videoSet:
				video.filePath = '{0:s}{1:s}'.format(settings.MEDIA_URL, video.filePath)
			videoList.append(videoSet)
		finally:
			return videoList

class Logout(generic.View):
	""" This view does not render any pages, but it handles when the user logs out.  It redirects back to the index.
		The user definitely gets logged out, but previous pages are in cache and can be reached by hitting the 
		browser's back button.  The documentation contains much info how to handle this for function based views,
		but the documentation for class based views is lacking.  This can get fixed with a little work.
	"""
	def get(self, request):
		#import pdb; pdb.set_trace()
		logout(request)
		return HttpResponseRedirect('/')

class UploadFiles(generic.View):
	"""
		This view does not render any pages.  It handles files submitted from the user's repository page.
		We choose to not use a template with FileField members for two reasons:  1) Django does not support multiple
		file inputs by default.  2) The file input widget on the html page does not work well with css.  So we
		created widgets on the html page that support multiple files and respond well to css.

		The view applies a series of validation rules prior to adding the file to the repository.
		Validation rules prior to uploading the media files:
			1) A manifest file has been loaded.
			2) The manifest file is xml.
			3) The file names loaded exactly match the files identified in the manifest.
			4) Verify each file's md5 signature
			5) Any non-unique files will generate a warning, but all others will be added.
	"""
	template_name = "videoRepository/uploadResponse.html"
	
	def __init__(self):
	    self.serverMessages = []

	def _readFileIn(self, requestedFile):
		md5Signature = hashlib.md5()
		mediapath = os.path.join(settings.TEMP_DIR, requestedFile.name)
		with open(mediapath, 'wb+') as destination:
			for chunk in requestedFile.chunks():
				md5Signature.update(chunk)
				destination.write(chunk)
		return md5Signature.hexdigest()

	def _validateFilesInManifest(self, xmlRoot, fileList):
		# We are simply going to guarantee that each file in the manifest is in fact uploaded.
		# If the user uploaded a file not in the manifest, we will simply ignore it.
		allMatch = True		
		for fname in xmlRoot.iter('filename'):
			match = False
			for i in range(len(fileList)):
				if fileList[i].name == fname.text:
					match = True
					break
			if match == False:
				allMatch = False
				self.serverMessages.append('\'{0:s}\' is in the manifest but was not uploaded.'.format(fname.text))
		return allMatch

	def _validateMD5Signatures(self, xmlRoot, fileList):
		allSignsValid = True
		for i in range(len(fileList)):
			signValid = False
			signature = self._readFileIn(fileList[i])
			for fileElement in xmlRoot:
				if fileElement.find('filename').text == fileList[i].name:
					if fileElement.find('md5').text == signature:
						signValid =  True
					break
			if signValid == False:
				allSignsValid = False
				self.serverMessages.append('\'{0:s}\' has an invalid md5 signature.'.format(fileList[i].name))
		return allSignsValid

	def _addFilesToRepository(self, xmlRoot, fileList, person, username, manifestname):
		# This function assumes all elements are present in each node.  We could write some defensive code, but
		# the exercise defines the format given, so we'll bypass that overhead.
		#import pdb; pdb.set_trace()
		for fileElement in xmlRoot:
			success = True
			filename = fileElement.find('filename').text
			filepath = '{0:s}/{1:s}'.format(username, filename)
			dateElements = fileElement.find('releasedate').text.split('/')
			releasedate = datetime.date(int(dateElements[2]), int(dateElements[0]), int(dateElements[1]))
			video = Video(	person=person,
							title=fileElement.find('title').text,
							version=fileElement.find('version').text,
							releaseDate=releasedate,
							contentType=fileElement.find('contenttype').text,
							language=fileElement.find('language').text,
							barCode=fileElement.find('barcode').text,
							md5=fileElement.find('md5').text,
							fileName=filename,
							filePath=filepath	)
			try:
				video.save()
			except:
				success = False
				self.serverMessages.append('The video \'{0:s}\' has a duplicate filename \'{1:s}\' and will not be added.'.format(video.title, filename))
			finally:
				old = os.path.join(settings.TEMP_DIR, filename)
				new = os.path.join(settings.MEDIA_ROOT, username, filename)
				os.rename(old, new)
		manifest = os.path.join(settings.TEMP_DIR, manifestname)
		os.remove(manifest)
		if success == False:
			self.serverMessages.append('Files not listed here were successfully added.')
		return success

	def post(self, request, username):
		if(request.user.is_authenticated() and request.user.username == username):
			fullName = '{0:s} {1:s}'.format(request.user.first_name, request.user.last_name)
			try:
				if request.FILES['selectManifest'].content_type == 'text/xml':
					self._readFileIn(request.FILES['selectManifest'])
				else:
					raise NotXMLException
			except NotXMLException:
				self.serverMessages.append('The loaded manifest is not a valid XML file.')
			except:
				self.serverMessages.append('The XML manifest was not loaded.')
			else:
				manifest = os.path.join(settings.TEMP_DIR, request.FILES['selectManifest'].name)
				xmlTree = ElementTree.parse(manifest)
				xmlRoot = xmlTree.getroot()
				fileList = request.FILES.getlist('selectVideoFiles')
				if self._validateFilesInManifest(xmlRoot, fileList):
					if self._validateMD5Signatures(xmlRoot, fileList):
						if self._addFilesToRepository(xmlRoot, fileList, request.user.person, username, request.FILES['selectManifest'].name):
							return HttpResponseRedirect('/UserRepository/{0:s}'.format(username)) # Redirect after POST - Success!

			# If we get here, we've fallen out of all of the try and if blocks above because there is an issue with the upload.
			# We direct the user to a form that can display the error messages.
			return render(	request,
							'videoRepository/uploadResponse.html',
							{'serverMessages':self.serverMessages, 'fullName':fullName, 'username':username}	)

		# User is not correct or not authenticated, so in this case, we'll bounce back to the index.		
		else:
			return HttpResponseRedirect('/')


