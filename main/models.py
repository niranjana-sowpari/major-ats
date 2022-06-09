from django.db import models

# Create your models here.
class Todolist(models.Model):
	name = models.CharField(max_length = 200)

	def __str__(self):
		return(self.name)

class Item(models.Model):
	todolist = models.ForeignKey(Todolist,on_delete = models.CASCADE)
	item = models.CharField(max_length = 300)
	boole = models.BooleanField()

	def __str__(self):
		return(self.item)
