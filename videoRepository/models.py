from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import datetime

# Default values that can be used project wide.
DEF_CHAR_FIELD_SIZE = 200
LARGE_CHAR_FIELD_SIZE = 2048
SMALL_CHAR_FIELD_SIZE = 32
COMPANY_VIDEO_PATH = 'company_videos'

class Person(models.Model):
	"""	This class represents a person who has a repository.  Most of the personal information is kept in the
		built in 'User' class.  This model has a one-to-one relationship with a 'User'.  It also has a one to
		many relationship with the videos the user has uploaded.
	"""
	#(Foreign Key - Video)
	user = models.OneToOneField(User)

	def __unicode__(self):
		return 'Person: {0:s}'.format(self.user)

class Video(models.Model):
	""" This class represents videos that are in a many to one relationship with a person.  It contains model
		fields for all of the meta data that is uploaded in the upload manifest.
	"""
	person = models.ForeignKey('Person')

	title = models.CharField('Title', max_length=DEF_CHAR_FIELD_SIZE)
	version = models.CharField('Version', max_length=SMALL_CHAR_FIELD_SIZE)
	releaseDate= models.DateField('Release Date')
	contentType = models.CharField('Content Type', max_length=SMALL_CHAR_FIELD_SIZE)
	language = models.CharField('Language', max_length=SMALL_CHAR_FIELD_SIZE)
	barCode = models.BigIntegerField('Bar Code')
	md5 = models.CharField('md5', max_length=SMALL_CHAR_FIELD_SIZE)
	fileName = models.CharField('File Name', max_length=DEF_CHAR_FIELD_SIZE)
	filePath = models.CharField('File Path', max_length=DEF_CHAR_FIELD_SIZE, unique=True)

	def __unicode__(self):
		return 'Video: {0:s}'.format(self.title)

