from django.shortcuts import redirect, render
import os,fnmatch
from zonemanage import *
from forms import *

def home(request):
	""" List the main index page for ZoneManage """
	msg=["Welcome to Zonemanage"]
	return render(request, "index.htm" , {'data' : msg})

def view_zone_list(request):
	""" List the main index page for ZoneManage """
	zone_array = [f for f in os.listdir(zonedir) if len(f) > 2 and f[0] not in ('.', '_')]
	zone_array = [f for f in os.listdir(zonedir) if fnmatch.fnmatch(f,'*.arpa') or fnmatch.fnmatch(f,'glam.*')]
	return render(request, "list_server_zones.htm",{ "zone_array" : zone_array})


def view_zone_detail(request,zonename):
	"""Get the details of the zone"""
	z=get_zone(zonename)
	soa_fields=soa_detail(z)
	hostnames = sorted_hostnames(zonename, z.names.keys())
	zone_data=dns_records(z,hostnames)
	return render(request, "zone_data.htm", { "zone_name" : zonename,"zone_data" : zone_data,"soa_fields" : soa_fields})

def edit_soa(request,zonename):
	"""Edit the SOA details of the zone"""
	z=get_zone(zonename)
	soa_fields=soa_detail(z)
    	if request.method == 'POST': # If the form has been submitted...
        	form = SOAForm(request.POST) # A form bound to the POST data
	        if form.is_valid(): # All validation rules pass
                        soa_fields = form.cleaned_data
                        status=savesoa(zonename,soa_fields)
			msg=[zonename + " saved Successfully. However you need to reload the RNDC to make it effective."]
			A='/reloadzone/'+zonename
			URL='Reload Zone'
                        return render(request, "index.htm" , {"data" : msg , 'URL' : URL ,'A' : A } )
	else:
	        form = SOAForm(initial=soa_fields) # An unbound form

	return render(request, 'edit_soa.htm', {'form': form,"zone_name" : zonename})


def edit_zone(request,zonename):
	"""Edit the Zone details of the zone"""
	z=get_zone(zonename)
	hostnames = sorted_hostnames(zonename, z.names.keys())
	zone_data=dns_records(z,hostnames)
	types=SUPPORTED_RECORD_TYPES
	return render(request, "edit_zone.htm", { "zone_name" : zonename,"zone_data" : zone_data, "types" : types })

def edit_zone1(request,zonename):
	"""Edit the Zone details of the zone"""
	z=get_zone(zonename)
	hostnames = sorted_hostnames(zonename, z.names.keys())
	zone_data=dns_records(z,hostnames)
	types=SUPPORTED_RECORD_TYPES
	

    	if request.method == 'POST': # If the form has been submitted...
	        email_formset = email_formset(request.POST)
        	form = RecordsForm(request.POST) # A form bound to the POST data
	        if form.is_valid() and email_formset.is_valid(): 
	            # Process the data in form.cleaned_data
	            # ...
	            return HttpResponseRedirect('/') # Redirect after POST
	else:
		formset = RecordsFormSet(initial=zone_data['zones'])

	return render(request, "edit_zone1.htm", { "zone_name" : zonename,"form" : formset })


def save_zone(request,zonename):
	"""Save the Zone details of the zone"""
	return render(request, "save_zone.htm" )

def reload_zone(request,zonename):
	"""Save the Zone details of the zone"""
	status=reload(zonename)
	data=[status,"Reload of zone "+zonename+" Successfull"]
	return render(request, "index.htm",{"data" : data } )
