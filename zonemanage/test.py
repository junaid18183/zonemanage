from zonemanage import *
from django.forms.formsets import formset_factory
from forms import RecordsForm
from django.conf import settings

settings.configure()

RecordsFormset = formset_factory(RecordsForm,extra=0)
formset = RecordsFormset()
formset = RecordsFormset(initial=[{"hostname" : "Juned","type" : "A" , "value":"192.168.3.10" , 'preference':'100'}])

#print formset.errors

#print "is Formset Valid", formset.valid()

#for form in formset:
#	print "form is", form
#	print "is form valid?",form.is_valid()
#	print "form error " , form.errors
#	#print "form cleaned data" ,form.cleaned_data

for form in formset.forms:
	if form.is_valid():
		print(form.cleaned_data)
	else:
		print "Juned"
		print form.errors

