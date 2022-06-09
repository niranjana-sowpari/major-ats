from django import forms

class upload_file(forms.Form):
	file = forms.FileField()
	#image = forms.ImageField()