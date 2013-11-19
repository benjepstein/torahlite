from django.db import models

class Leyner(models.Model):
	'''
	Defines a Leyner.

	FIELDS:

	name: string, name of leyner
	total_verses_read:  integer, sum total of verses read
	'''

	name = models.CharField(max_length=200)
	total_verses_read = models.IntegerField(default=0)
	def __unicode__(self):
		return self.name

class Parasha(models.Model):
	'''
	Defines a parasha.
	
	FIELDS:
	
	name: string, name of the parasha 
	parasha_length: integer, number of pesukim
	'''
	name = models.CharField(max_length=20)
	parasha_length = models.IntegerField(default=0)
	#leyner = models.ForeignKey(Leyner, null=True, blank=True)
	def __unicode__(self):
		return self.name


class Aliyah(models.Model):
	'''
	Defines an Aliyah.
	
	FIELDS:
	
 	start_chapter = integer, start chapter
 	start_verse = integer, start verse
 	end_chapter = integer, end chapter
 	end_verse = integer, end verse
 	aliyah_length = integer, total number of verses
 	parasha = ForeignKey to Parasha
 	leyner = ForeignKey to Leyner
 	number = Aliyah number (1-7,M for maftir)
	'''

 	ALIYAH_CHOICES = (
 		(1,"Rishon"),
 		(2,"Sheni"),
 		(3,"Shlishi"),
 		(4,"Revi'i"),
 		(5,"Chamishi"),
 		(6,"Shishi"), 
 		(7,"Shvi'i"),
 		(8,"Maftir"),
 		)
 	#start_chapter = models.IntegerField(default=0)
 	start_verse = models.IntegerField(default=0)
 	#end_chapter = models.IntegerField(default=0)
 	end_verse = models.IntegerField(default=0)
 	aliyah_length = models.IntegerField(default=0)
 	parasha = models.ForeignKey(Parasha)
 	leyner = models.ForeignKey(Leyner,blank=True, null=True)
 	#dateread = models.DateField()
 	number = models.IntegerField(choices=ALIYAH_CHOICES)
	def __unicode__(self):
 		return str(self.parasha)+", Aliyah "+str(self.number)
