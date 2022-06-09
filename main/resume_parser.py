'''pip install pyresparser

# spaCy
python -m spacy download en_core_web_sm

# nltk
python -m nltk.downloader words'''

import nltk

from nltk.corpus import stopwords

from pyresparser import ResumeParser

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from django.conf import settings

import re



class class_res:

	def resume_fun(self, path):

		#path = "/content/Niranjana Sowpari Resume (October 2021).pdf"

		#nltk.download('stopwords')  ### run this on python shell

		
		x = "local path"
		
		#value = str(settings.BASE_DIR)
		#x = value + path
		x = x + path
		
		'''print("----------------------------------------",value)
		print("----------------------------------------",path)'''

		#x = os.path.join(settings.BASE_DIR, path)

		#new_value = re.sub("\\", "/", value)

		#value.replace('\\','/')

		#print("----------------------------------------",value)

		'''print("----------------------------------------",type(settings.BASE_DIR))

		print("----------------------------------------",type(value))

		print("----------------------------------------",x)'''
		
		data = ResumeParser(x).get_extracted_data()
						
		sk_ls = data["skills"]
						
		res = ''
						
		for ele in sk_ls:
			res = res + ele + " "
		
		return res