from django.shortcuts import render
from django.http import HttpResponse
from . models import Todolist, Item
from . forms import upload_file
from django.core.files.storage import FileSystemStorage
from . resume_parser import class_res
from pyresparser import ResumeParser
from . webscrapped import class_webScrap
import pandas as pd
from . score_cal import *

# Create your views here.


def dataframe(response):
	l1 = ["1","2","3","4","5"]
	l2 = ["Niranjana","Jungkook","Taehyung","Jimin","Namjoon"]
	links = ["https://www.google.com/","https://www.google.com/","https://www.google.com/","https://www.google.com/","https://www.google.com/"]

	en_labels = list(zip(l1,l2,links))
	df = pd.DataFrame(en_labels)
	df.columns = ["Sno","Names","links"]


	def make_clickable(links):
		return '<a target="_blank" href="{}"> {} </a>'.format(links,links + "helllllloooo")

	
	#df['Names'] = df.apply(lambda x: make_clickable(x['Sno'], x['Names']), axis=1)

	df.style.format({'links':make_clickable})


	dict2 = {
		'dfi':df.to_html(render_links = True)
	}

	return render(response, "main/df.html", dict2)



def index(response, name):
	#return HttpResponse("<h1>Application tracking system</h1>")
	t = Todolist.objects.get(name = name)
	#ls = t.item_set.get(id = 1)
	#return HttpResponse("<h1>%s</h1><br><br><h4>%s</h4>" %(t.name, str(ls.item)))
	return render(response, "main/base.html" , {"t":t})


def home(response):
	my_dict = {"name1":"Niranjana", "name2":"Jungkook", "name3":"Jimin"}
	return render(response, "main/sample.html" , my_dict)



def web_scrap_jd(response):
	ob = class_webScrap()
	ob.fun_each_link()

	'''print("Companies: ", ob.company_name)
				print(len(ob.company_name))
			
				print("Job titles: ", ob.job_title)
				print(len(ob.job_title))
			
				print("Location: ", ob.location)
				print(len(ob.location))'''

	en_labels = list(zip(ob.company_name,ob.job_title,ob.location,ob.job_links))
	df = pd.DataFrame(en_labels)
	df.columns = ["Company","Job Title","Location","Link"]


	df['Link'] = df['Link'].apply(lambda x: f'<a href="{x}" target="_blank">    Click Here   </a>')

	df['jd']=ob.job_description

	df=df[df['jd']!='']

	dict2 = {
		'dfi':df.to_html(render_links = True, escape = False)
	}


	return render(response, 'main/df.html' , dict2)



def form(response):
	context = {}

	if response.method == 'POST':

		uploaded_file = response.FILES['doc']
		fs = FileSystemStorage()

		new_name = fs.save(uploaded_file.name , uploaded_file)

		context['url'] = fs.url(new_name)

		res_ob = class_res()

		resume_skills = res_ob.resume_fun(fs.url(new_name))

		context['skills'] = resume_skills

		#print("FILE NAME ==========" , uploaded_file.name)
		#return render(response, "main/test.html" , {"file":uploaded_file})
	
		#form = upload_file()

	return render(response , "main/forms.html" , context)


def final(response):
	f_dict = {}


	#####   RESUME PARSER

	if response.method == 'POST':

		uploaded_file = response.FILES['doc']
		fs = FileSystemStorage()

		new_filename = fs.save(uploaded_file.name , uploaded_file)

		

		'''try_new = "C:/Users/RIMA/Desktop/Django/mysite/media/"
						
								try_new = try_new + new_filename'''

		#f__name = {}

		#f__name['val'] = fs.url(new_filename)

		#return render(response,"main/blank.html", f__name)

		#print("----------------------", dict2['url'])

		res_ob = class_res()

		#print("===============================",fs.url(new_filename) )

		resume_skills = res_ob.resume_fun(fs.url(new_filename))

		#dict2['skills'] = resume_skills


	#####   JOB DESCRIPTION

			
		ob = class_webScrap()
		ob.fun_each_link()


		

		#df['Job Description']=ob.job_description

		#df=df[df['jd']!='']


		

		#####   NLTK

		sc_list = []
		sc = class_score()

		#print(ob.jd_ne)

		for ele in ob.jd_ne:
			new_list = [resume_skills, ele]		
			ans = sc.fun_sc(new_list)

			sc_list.append(ans)


		en_labels = list(zip(ob.company_name,ob.job_title,ob.location,ob.job_links,sc_list))
		df = pd.DataFrame(en_labels)
		df.columns = ["Company","Job Title","Location","Link","Scores (in percentage)"]


		df['Link'] = df['Link'].apply(lambda x: f'<a href="{x}" target="_blank">    Click Here   </a>')

		#df['Scores (in percentage)'] = sc_list

		#print("-----------------------------------------", sc_list)


		old_df = df.sort_values("Scores (in percentage)", ascending = False)

		new_df = old_df.head(10)

		#new_df.drop("Job Description" , axis = 1 , inplace = True)

		#print("-------------",type(sc_list[0]))

		f_dict = {
			'dfi':new_df.to_html(render_links = True, escape = False)
		}

		f_dict['url'] = fs.url(new_filename)

	return render(response , "main/final.html" , f_dict)
	

