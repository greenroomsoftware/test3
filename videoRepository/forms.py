from django import forms

from videoRepository import models

class LoginForm(forms.Form):
	""" Login Form for the Video Respository Index """
	loginusername = forms.CharField(	max_length=models.SMALL_CHAR_FIELD_SIZE,
										label='User Name',
										widget=forms.TextInput(attrs={'placeholder':'User Name', 'autofocus':'true'})	)
	loginpassword = forms.CharField(	max_length=models.SMALL_CHAR_FIELD_SIZE,
										label='Password',
										widget=forms.PasswordInput(attrs={'placeholder':'Password'})	)


class NewUserForm(forms.Form):
	""" New User Form for the Video Respository Index """
	newfirstname = forms.CharField(	max_length=models.SMALL_CHAR_FIELD_SIZE,
									label='First Name',
									widget=forms.TextInput(attrs={'placeholder':'First Name', 'autofocus':'true'})	)
	newlastname = forms.CharField(	max_length=models.SMALL_CHAR_FIELD_SIZE,
									label='Last Name',
									widget=forms.TextInput(attrs={'placeholder':'Last Name'})	)
	newusername = forms.CharField(	max_length=models.SMALL_CHAR_FIELD_SIZE,
									label='User Name',
									widget=forms.TextInput(attrs={'placeholder':'User Name'})	)
	newpassword = forms.CharField(	max_length=models.SMALL_CHAR_FIELD_SIZE,
									label='Password',
									widget=forms.PasswordInput(attrs={'placeholder':'Password'})	)

