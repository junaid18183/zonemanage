import os
import shutil
import logging
import fnmatch

from easyzone import Zone,ZoneCheck,ZoneReload,ZoneReloadError
from config import *

#---------------------------------------------------------------------------------------------------------------
CHANGE_TYPE_SAVE = 'S'
CHANGE_TYPE_RELOAD = 'R'
CHANGE_TYPE_REVERT = 'V'
CHANGE_TYPES = (CHANGE_TYPE_SAVE, CHANGE_TYPE_RELOAD, CHANGE_TYPE_REVERT)
#---------------------------------------------------------------------------------------------------------------
def get_zone_list():
	#zonedir is the direcory location defined in configuration
	zone_array = [f for f in os.listdir(zonedir) if len(f) > 2 and f[0] not in ('.', '_')]
	zone_array = [f for f in os.listdir(zonedir) if fnmatch.fnmatch(f,'*.arpa') or fnmatch.fnmatch(f,'glam.*')]
	return zone_array
#---------------------------------------------------------------------------------------------------------------
def get_zone_archive_list(zonename):
	#archive_dir is the direcory location defined in configuration
	zone_array = [f for f in os.listdir(archive_dir) if fnmatch.fnmatch(f,zonename+".*")]
	soa_array = [ i.split(zonename,1)[1][1:] for i in zone_array]
	records = [ i.split("-") for i in soa_array ]
	
	return records
#---------------------------------------------------------------------------------------------------------------
def get_zone(zonename):
	'''Return a Zone instance for zonename that has been loaded
	from the actual zone file.
	If the zone file cannot be found or loaded, a redirect to "/"
	is raised.
	'''

	z = Zone(zonename)
	zone_file = find_zone_file(zonedir, zonename)
	z.load_from_file(zone_file)
	return z

#---------------------------------------------------------------------------------------------------------------
def find_zone_file(zonedir, zonename):
	'''Find the zone file name by trying a few common
	extensions, including:
	* no extension ('example.com')
	* trailing dot ('example.com.')
	* .db ('example.com.db')
	* .zone ('example.com.zone')
	'''
	# remove any trailing dot
	if zonename[-1] == '.':
		zonename = zonename[:-1]
	extensions = ('', '.', '.db', 'zone','.arpa')
	for ext in extensions:
		zone_file = os.path.join(zonedir, zonename )
		#zone_file = os.path.join(zonedir, zonename + ext)
	if os.path.isfile(zone_file):
		return zone_file
	return None
#---------------------------------------------------------------------------------------------------------------
def sorted_hostnames(zonename, hostnames):
	if zonename in hostnames:
	    # sort hostnames but move root zone to start of list
	    del hostnames[hostnames.index(zonename)]
	    hostnames.sort()
	    hostnames.insert(0, zonename)
	else:
	    # sort hostnames
	    hostnames.sort()

	return hostnames
#---------------------------------------------------------------------------------------------------------------
def check_zone(zonename, zonefile):
	'''Check the syntax of a zonefile by calling the named-checkzone
	binary defined in the config 'checkzone'.
	If 'checkzone' is not defined then this check is disabled
	(it always returns True).
	'''
	if checkzone_path is None:
	    # skip the check
	    return True

	c = ZoneCheck(checkzone_path)
	r = c.isValid(zonename, zonefile)
	if not r:
	    msg=("ZoneCheck failed for zone='%s' file='%s' error was: %s" %(zonename, zonefile, c.error))
	return r
#---------------------------------------------------------------------------------------------------------------
def archive_zone(zone,uid):
	'''Copies a zone file to the archive directory defined in config
	by "archive_dir".

	Returns the filename (not including path) of the archived file.

	If "zoner.archive_dir" is not defined then nothing will be archived
	and this function will return None.
	'''
	if archive_dir is None:
	    return None

	if not uid:
		uid='admin'

	filename = zone.domain + str(zone.root.soa.serial) + "-" + uid
	full_path = os.path.join(archive_dir, filename)

	if os.path.exists(full_path):
	    # this is an unusual situation
	    raise Exception("archive_zone() failed as archived file already exists: %s" %full_path)

	shutil.copyfile(zone.filename, full_path)
	return filename

#---------------------------------------------------------------------------------------------------------------
def get_archive(zonename, filename):
	'''Return a Zone instance for zonename that has been loaded
	from an archived zone file filename.
	If the zone file cannot be found or loaded, a redirect to "/"
	is raised.
	'''
	z = Zone(zonename)
	if archive_dir is None:
		raise Exception("archive_dir is not not defined, please check the configuration")
	zone_file = find_zone_file(archive_dir, filename)
	if not zone_file:
	   raise Exception("Archived zone file does not exist")

	z.load_from_file(zone_file)
	return z
#---------------------------------------------------------------------------------------------------------------
def revert(zone,archive,uid):
	z = get_zone(zone)
	za = get_archive(zone, archive)
	archive_serial = za.root.soa.serial
	archive_file = archive_zone(z,uid)

	za.root.soa.serial = z.root.soa.serial
	za.save(filename=z.filename, autoserial=True)

	msg=["Zone reverted back from archive %s"  %archive]
	return msg
#---------------------------------------------------------------------------------------------------------------
def reload(zone):
	z = get_zone(zone)
	if not check_zone(z.domain, z.filename):
		raise Exception ("Zone file failed syntax check, please examine:", z.filename)
	else:
		if rndc_path is None:
			msg="Reload signalling is disabled. Set 'zoner.rndc' in the config to enable."
		else:
	       		zr = ZoneReload(rndc=rndc_path)
			try:
	               		zr.reload(z.domain)
	                except ZoneReloadError, err:
		               	raise Exception("zone reload failed: %s",err)
			else:
	                	msg="named has been signalled to reload zone:"+z.domain
	return msg

#---------------------------------------------------------------------------------------------------------------
def savesoa(zone,soa_fields,uid):
	    z = get_zone(zone)
	    soa = z.root.soa
	    soa.mname = soa_fields['mname']
	    soa.rname = soa_fields['rname']
	    soa.refresh = soa_fields['refresh']
	    soa.retry = soa_fields['retry']
	    soa.expire = soa_fields['expire']
	    soa.minttl = soa_fields['minttl']
	    if soa.serial == soa_fields['serial']:
	        auto_inc_serial = True
	    else:
	        auto_inc_serial = False
	        soa.serial = soa_fields['serial']

	    archive_file = archive_zone(z,uid)
	    archive_serial = z.root.soa.serial

	    try:
	        z.save(autoserial=auto_inc_serial)
	    except Exception, e:
		raise Exception (str(e))
	        auto_inc_serial = False
	    else:
	        if not check_zone(z.domain, z.filename):
	            msg="Zone was saved but failed syntax check. Please examine file:"+z.filename
	        else:
		    msg=z.domain + " saved Successfully. However you need to reload the RNDC to make it effective.The original zone is preserved as " + archive_file

	    return msg

#---------------------------------------------------------------------------------------------------------------
def savezone(zone,z_records,uid ):
	z = get_zone(zone)
	save_ok = True
	auto_inc_serial = False
	
	# remove existing nodes
	names = z.names.keys()
	names.remove(z.domain)  # remove '@' (root)
	for name in names:
		z.delete_name(name)
		# delete nodes from '@' but don't remove it completely (otherwise SOA is gone...)
		root = z.root
	   	root.clear_all_records(exclude='SOA')

	# replace with values submitted from form
	for record in z_records:
		hostname = record['hostname']
	        rtype = record['type']
	        preference = 10
	        #preference = record['preference']  #commented on 15May
	        value = record['value']

	        if hostname and value and rtype in SUPPORTED_RECORD_TYPES:
		        #if hostname not in z.names.keys():
			if save_ok : # Just for if indent 
	        	        z.add_name(hostname)
	            		name = z.names[hostname]
	            		if rtype == 'MX':
					 name.records(rtype, create=True).add( (int(preference), str(value)) )
	            		else:
					 name.records(rtype, create=True).add(str(value))
	        else:
	        	save_ok = False
			msg=["Save_Ok failed"]

	if save_ok:
		archive_file = archive_zone(z,uid)
	        archive_serial = z.root.soa.serial
	        auto_inc_serial = True
	        z.save(autoserial=auto_inc_serial)
	        if not check_zone(z.domain, z.filename):
	        	msg=["Zone was saved but failed syntax check. Please examine file: %s" %z.filename]
	        else:
	            	msg=["Zone %s has been saved. Don't forget to signal named to reload the zone.The original copy is preserved as %s" % (z.domain,archive_file)]
	return msg	

#---------------------------------------------------------------------------------------------------------------
def soa_detail(z):
	soa = z.root.soa
        soa_fields = {
                    'zone' : z.domain,
                    'mname' : soa.mname,
                    'rname' : soa.rname,
                    'serial' : soa.serial,
                    'refresh' : soa.refresh,
                    'retry' : soa.retry,
                    'expire' : soa.expire,
                    'minttl' : soa.minttl,
                }
	return soa_fields
#---------------------------------------------------------------------------------------------------------------
def dns_records(z,hostnames):
	values = dict(
		zones = [],
		)
	for host in hostnames:
		for ntype in SUPPORTED_RECORD_TYPES:
	        	node = z.names[host].records(ntype)
	        	if node:
        			for record in node.items:
					data = dict(hostname = host,type = ntype,value = record ,preference = '',)
	        	        	if ntype == 'MX':
        	     				data['preference'] = record[0]
			                  	data['value'] = record[1]
					values['zones'].append(data)
	return values
#---------------------------------------------------------------------------------------------------------------
