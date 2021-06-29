from django import forms
from .models import CANDIDATE, INTERVIEW
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

LANGUAGE_CHOICES = ( ('English', 'English'), ('Hindi', 'Hindi'), ('Kannada','Kannada'), ('Marathi', 'Marathi') )

fileFormats = ['mp3', 'mp4', 'wav', 'm4a']


class DateInput(forms.DateInput):

	input_type = 'date'




class UserLoginForm(forms.Form): 
    
	username = forms.CharField(required = True, max_length = 30)
	password = forms.CharField(widget = forms.PasswordInput(), required = True)

    
class INTERVIEWForm(forms.ModelForm):

	interview_File = forms.FileField(required = True)
	language_Of_Submission = forms.CharField( required = True, widget = forms.Select( choices = LANGUAGE_CHOICES ) )

	class Meta:

		model = INTERVIEW
		fields = []
    	

	#overriding clean method
	def clean(self):
	
		cleaned_data = super().clean()
		
		tempList = cleaned_data['interview_File'].name.split(".")
		
		if(tempList[-1].strip() not in fileFormats):
		
			raise ValidationError( ('Invalid File Format, only : {0} accepted'.format(', '.join(fileFormats))), code='invalid_file_format')
		
			
		return cleaned_data
