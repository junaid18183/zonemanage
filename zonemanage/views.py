from django.http import HttpResponse,Http404
from django.shortcuts import redirect, render
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

from zonemanage import *
from forms import *



def logout_view(request):
    logout(request)
    msg=["Logged Out Successfully"]
    return render(request, "index.htm" , {'data' : msg})

def home(request):
	""" List the main index page for ZoneManage """
	msg=["Welcome to Zonemanage"]
	return render(request, "index.htm" , {'data' : msg})


@login_required
def view_zone_list(request):
	""" List the main index page for ZoneManage """
	zone_array = get_zone_list()
	return render(request, "list_server_zones.htm",{ "zone_array" : zone_array})


@login_required
def view_zone_detail(request,zonename):
	"""Get the details of the zone"""
	z=get_zone(zonename)
	soa_fields=soa_detail(z)
	hostnames = sorted_hostnames(zonename, z.names.keys())
	zone_data=dns_records(z,hostnames)
	return render(request, "zone_data.htm", { "zone_name" : zonename,"zone_data" : zone_data,"soa_fields" : soa_fields})

@login_required
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
			A='/zonemanage/reloadzone/'+zonename
			URL='Reload Zone'
                        return render(request, "index.htm" , {"data" : msg , 'URL' : URL ,'A' : A } )
		else:
			data=[formset.errors]
                        return render(request, "index.htm" , {"data" : data } )

	else:
	        form = SOAForm(initial=soa_fields) # An unbound form
		return render(request, 'edit_soa.htm', {'form': form,"zone_name" : zonename})


@login_required
def edit_zone(request,zonename):
	"""Edit the Zone details of the zone"""
	z=get_zone(zonename)
	hostnames = sorted_hostnames(zonename, z.names.keys())
	zone_data=dns_records(z,hostnames)
	types=SUPPORTED_RECORD_TYPES
	z_records=[]	
	RecordsFormSet = formset_factory(RecordsForm, extra=0)
	
    	if request.method == 'POST': # If the form has been submitted...
       		formset = RecordsFormSet(request.POST) # A form bound to the POST data
        	if formset.is_valid(): 
			for form in formset:
				if form.is_valid():
					z_records.append(form.cleaned_data)
	
			data=savezone(zonename,z_records)
			A='/zonemanage/reloadzone/'+zonename
                       	URL='Reload Zone'
		else:
			data=[formset.errors]
			A='/zonemanage/editzone/'+zonename
			URL='Edit Zone'
               	return render(request, "index.htm" , {"data" : data , 'URL' : URL ,'A' : A } )
			
	else:
		formset = RecordsFormSet(initial=zone_data['zones'])
		return render(request, "edit_zone.htm", { "zone_name" : zonename,"formset" : formset })


@login_required
def save_zone(request,zonename):
	"""Save the Zone details of the zone"""
	return render(request, "save_zone.htm" )

@login_required
def reload_zone(request,zonename):
	"""Save the Zone details of the zone"""
	status=reload(zonename)
	data=[status,"Reload of zone "+zonename+" Successfull"]
	A='/zonemanage/zone_detail/'+zonename
	URL=zonename
	return render(request, "index.htm",{"data" : data , 'URL' : URL ,'A' : A } )


@login_required
def archive_list(request,zonename):
	zone_array = get_zone_archive_list(zonename)
        return render(request, "archieve_list.htm",{ "zone_array" : zone_array,"zonename":zonename})
	
@login_required
def load_archive(request,zonename,archive_soa):
	arch_file=zonename+"."+archive_soa
	z=get_archive(zonename,arch_file)
	soa_fields=soa_detail(z)
        hostnames = sorted_hostnames(zonename, z.names.keys())
        zone_data=dns_records(z,hostnames)
        return render(request, "archieve_zone_data.htm", { "zone_name" : zonename,"zone_data" : zone_data,"soa_fields" : soa_fields, "archive":arch_file})
