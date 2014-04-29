from django import forms

class SOAForm(forms.Form):
    mname = forms.CharField(label='Master Name Server')
    rname = forms.CharField(label='Admin Email')
    #serial = forms.IntegerField(widget=forms.NumberInput(attrs={'disabled':'True'}))
    #serial = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':'True'}))
    serial = forms.IntegerField(widget=forms.NumberInput)
    refresh = forms.IntegerField()
    retry = forms.IntegerField()
    expire = forms.IntegerField()
    minttl = forms.IntegerField()


class RecordsForm(forms.Form):
	hostname = forms.CharField(label='HostName')
	type = forms.CharField ( label='Record Type')
	value = forms.CharField ( label='Value')
