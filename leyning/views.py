from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django import forms
import datetime
import hebcalparser
#import bible

from leyning.models import Parasha, Leyner, Aliyah

class LeynerForm(forms.Form):
	'''
	Single leyner choice form.
	'''
	leyner = forms.ModelChoiceField(queryset=Leyner.objects.all())

class AliyahLeynerForm(forms.Form):
	'''
	Select Form for choosing a leyner for each of the seven aliyot.
	Provides all Leyners in the database as options in the dropdown box.
	'''
	aliyah_1 = forms.ModelChoiceField(queryset=Leyner.objects.all(), required=False)
	aliyah_2 = forms.ModelChoiceField(queryset=Leyner.objects.all(), required=False)
	aliyah_3 = forms.ModelChoiceField(queryset=Leyner.objects.all(), required=False)
	aliyah_4 = forms.ModelChoiceField(queryset=Leyner.objects.all(), required=False)
	aliyah_5 = forms.ModelChoiceField(queryset=Leyner.objects.all(), required=False)
	aliyah_6 = forms.ModelChoiceField(queryset=Leyner.objects.all(), required=False)
	aliyah_7 = forms.ModelChoiceField(queryset=Leyner.objects.all(), required=False)

class DateForm(forms.Form):
	'''
	Date Form for inputting a date to pull parasha info from hebcal.
	Just type in the date, but it has to be in a standard date format:
	
	2006-10-25
	10/25/2006
	10/25/06

	'''
	date = forms.DateField()

def redirect_index(request):
	return redirect('/leyning/')

def hebcal_import(request):
	'''
	Converts date to the next Saturday and returns aliyah data on it.
	'''
	
	if request.method == "POST":
		my_date_form = DateForm(request.POST)
		new_date_form = DateForm()
		if my_date_form.is_valid():
			mydate = hebcalparser.converttosat(my_date_form.cleaned_data["date"])
			aliyot_info = hebcalparser.getaliyahdata(mydate)["aliyot"]
			context = {
			'aliyot': aliyot_info,
			'date':mydate,
			'form':new_date_form
			}

	else:
		my_date_form = DateForm()
		context = {
		'form': my_date_form,
		'date':datetime.date.today()
		}

	return render(request, 'leyning/parashainfo.html',context)

def index(request):
	'''
	Displays a page with a list of all of the parshiyot.
	'''
	parasha_list = Parasha.objects.all()
	context = {'parasha_list':parasha_list}
	return render(request, 'leyning/index.html',context)

def index(request):
	'''
	Displays a page with a list of all of the parshiyot.
	'''
	date = hebcalparser.converttosat(datetime.date.today())
	parasha_list = Parasha.objects.all()
	parasha_name = hebcalparser.getaliyahdata(date)["parashaname"]
	parasha = Parasha.objects.get_or_create(name=parasha_name)[0]
	parasha.save()
	aliyah_list = []
	for aliyahnum in range(1,8):
		newaliyah = Aliyah.objects.get_or_create(parasha=parasha, number=aliyahnum)[0]
		newaliyah.save()
		aliyah_list.append(newaliyah)
	context = {
	'parasha_list':parasha_list,
	'date':date,
	'aliyah_list':aliyah_list,
	'parasha_name':parasha_name}
	return render(request, 'leyning/indexB.html',context)


def parasha_detail(request, parasha_name):
	'''
	Displays a page with info on the parasha.
	Shows the seven aliyot with the currently assigned leyner, and has a form
	that can be submitted for reassigning the leyners.
	'''

	myparasha = Parasha.objects.get(name=parasha_name)
	aliyahlist = []
	for aliyahnum in range(1,8):
		newaliyah = Aliyah.objects.get_or_create(parasha=myparasha, number=aliyahnum)[0]
		aliyahlist.append(newaliyah)
	
	if request.method == "POST":
		leyner_form = AliyahLeynerForm(request.POST)
		if leyner_form.is_valid():
			aliyahlabels = ["aliyah_1","aliyah_2","aliyah_3","aliyah_4","aliyah_5","aliyah_6","aliyah_7"]
			for i in range(0,7):
				try:
					newleyner = Leyner.objects.get(name=leyner_form.cleaned_data[aliyahlabels[i]])
				except:
					aliyahlist[i].leyner = None
					aliyahlist[i].save()
				else:
					aliyahlist[i].leyner = newleyner
					aliyahlist[i].save()
			return HttpResponse("Leyners updated!<br><a href='/leyning'>Home</a>")
		#newleyner = Leyner.objects.get(name=myleynername)
		#myparasha = Parasha.objects.get(name=parasha_name)
		#try:
		#	oldleyner = myparasha.leyner.name
		#except:
		#	oldleyner = "nobody"
		#myparasha.leyner = newleyner
		#myparasha.save()
		#if oldleyner == newleyner.name:
		#	return HttpResponse("No change!  The leyner is still "+str(myparasha.leyner.name)+".")	
		#else:
		#	return HttpResponse("Great!  The old leyner was "+oldleyner+", but the new leyner is "+str(myparasha.leyner.name)+".")

	else:
		leyner_form = AliyahLeynerForm(initial={
		'aliyah_1':aliyahlist[0].leyner,
		'aliyah_2':aliyahlist[1].leyner,
		'aliyah_3':aliyahlist[2].leyner,
		'aliyah_4':aliyahlist[3].leyner,
		'aliyah_5':aliyahlist[4].leyner,
		'aliyah_6':aliyahlist[5].leyner,
		'aliyah_7':aliyahlist[6].leyner
		})
	context = {'form':leyner_form,
	'parasha':myparasha,
	'aliyah_list':aliyahlist,
	'aliyahform':leyner_form
	}
	return render(request, 'leyning/pedit.html',context)
#	return HttpResponse("This is the info on Parashat %s." % parasha_name)

def leyner_detail(request, leyner_name):
	return HttpResponse("This is the info on Master Leyner %s." % leyner_name)	

#def hebcal_import(request):
#	return HttpResponse("This is where we will import hebcal data.")	
#def update_leyner(request):	
#	return render(request, )