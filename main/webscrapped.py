import requests
import bs4
import re
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag

class class_webScrap:

	company_name = []
	job_title = []
	location = []
	job_links = []
	job_description=[]
	jd_ne = []


	def fun_jd_ne(self):

		for jd in self.job_description:
			if len(jd)==0:
				self.jd_ne.append('')
				continue

			wt = word_tokenize(jd)

			l = []

			for i in wt:
				if i not in stopwords.words('english'):
					l.append(i)

			taggs = pos_tag(l)

			chunks = nltk.ne_chunk(taggs, binary=True) #either NE or not NE

			entities =[]
			labels =[]

			for chunk in chunks:
				if hasattr(chunk,'label'):
					entities.append(' '.join(c[0] for c in chunk))
					labels.append(chunk.label())

			jd = ''

			for i in entities:
				jd = jd + i + ' '


			self.jd_ne.append(jd)




	def fun_each_link(self):

		link4 = 'https://www.glassdoor.co.in/Job/software-engineering-jobs-SRCH_KO0,20.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&typedLocation=&context=Jobs&dropdown=0'
		link3 = 'https://www.glassdoor.co.in/Job/software-engineer-jobs-SRCH_KO0,17.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=software&typedLocation=&context=Jobs&dropdown=0'
		link1 = 'https://www.glassdoor.co.in/Job/data-science-jobs-SRCH_KO0,12.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=data%2520sc&typedLocation=&context=Jobs&dropdown=0'
		link2 = 'https://www.glassdoor.co.in/Job/information-technology-jobs-SRCH_KO0,22.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=informa&typedLocation=&context=Jobs&dropdown=0'

		#links = [link1, link2, link3, link4]
		links = [link3]

		for l in links:
			self.fun_get_data(l)

	def fun_get_data(self,l):
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'}
		req = requests.get(l,headers=headers)
		doc = bs4.BeautifulSoup(req.text,"html.parser")
		print(doc.title.text)

		## Company name


		for com in doc.findAll('div', {'class':'job-search-key-1mn3dn8'}):
			if com.text != '':
				self.company_name.append(com.findAll('a')[0].text)


		ind_ls = []
		for com in self.company_name:
			if re.search("^.job-search-key.*$",com):
				ind = self.company_name.index(com)
				ind_ls.append(ind)


		for i in reversed(ind_ls):
			del self.company_name[i]


		'''print("Companies: ", self.company_name)
								print(len(self.company_name))
						'''
		##  Job Title



		for com in doc.findAll('div', {'class':'job-search-key-1mn3dn8'}):
			if com.text != '':
				self.job_title.append(com.findAll('a')[1].text)


		ind_ls = []
		for com in self.job_title:
			if re.search("^.job-search-key.*$",com):
				ind = self.job_title.index(com)
				ind_ls.append(ind)


		for i in reversed(ind_ls):
			del self.job_title[i]


		'''print("Job Titles: ", self.job_title)
								print(len(self.job_title))
						'''

		##  Location



		for com in doc.findAll('div', {'class':'job-search-key-1mn3dn8'}):
			if com.text != '':
				x = com.findAll('div')[2]
				self.location.append(x.findAll('span')[0].text)


		ind_ls = []
		for com in self.location:
			if re.search("^.job-search-key.*$",com):
				ind = self.location.index(com)
				ind_ls.append(ind)


		for i in reversed(ind_ls):
			del self.location[i]


		'''print("Location: ", self.location)
								print(len(self.location))'''


		## Job Links


		for com in doc.findAll('div', {'class':'job-search-key-1mn3dn8'}):
			if com.text != '':
				x = com.findAll('div')[0]
				var = 'https://www.glassdoor.co.in' + x.a['href']
				self.job_links.append(var)
			


		ind_ls = []
		for com in self.job_links:
			if re.search("^.job-search-key.*$",com):
				ind = self.job_links.index(com)
				ind_ls.append(ind)


		for i in reversed(ind_ls):
			del self.job_links[i]


		### Job Description






		
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'}
		for i in self.job_links:
			req_desc = requests.get(i,headers=headers)
			soup = bs4.BeautifulSoup(req_desc.text,'html.parser')

			str = ''
			for doc in soup.findAll('p'):
				if re.search('^Copyright.*$',doc.text):
					pass
				else:
					str = str + doc.text + ' '

			self.job_description.append(str)


		self.fun_jd_ne()


		'''for i in reversed(self.job_description):
									if i == '':
										del i'''


		'''print("Job Links: ", self.job_links)
								print(len(self.job_links))'''





				
