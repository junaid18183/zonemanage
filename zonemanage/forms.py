from django import forms

from config import *

Record_Type = [ (i,i) for i in SUPPORTED_RECORD_TYPES ]

class SOAForm(forms.Form):
    mname = forms.CharField(label='Master Name Server')
    rname = forms.CharField(label='Admin Email')
    serial = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':'True'}))
    refresh = forms.IntegerField()
    retry = forms.IntegerField()
    expire = forms.IntegerField()
    minttl = forms.IntegerField()


class RecordsForm(forms.Form):
	hostname = forms.CharField(label='HostName')
	type = forms.ChoiceField( label='Record Type', choices=Record_Type)
	value = forms.CharField ( label='Value')
	preference = forms.CharField ( label='Preference',required=False)

