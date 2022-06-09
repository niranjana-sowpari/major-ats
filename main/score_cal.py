from sklearn.feature_extraction.text import CountVectorizer

from sklearn.metrics.pairwise import cosine_similarity

class class_score():

	def fun_sc(self,ls):
		cv = CountVectorizer()
		count_matrix = cv.fit_transform(ls)

		#print(ls)

		x = cosine_similarity(count_matrix)

		#score_ls.append(float(format((x[0][1] * 100),".2f")))
		#print(x)

		#print(" ---------- ", format((x[0][1] * 100),".2f"))
		
		return float(format((x[0][1] * 100),".2f"))