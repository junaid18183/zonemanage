from zonemanage import *
from django.forms.formsets import formset_factory
from forms import RecordsForm
from django.conf import settings

SUPPORTED_RECORD_TYPES=['NS']

settings.configure()

zonename='glam.com'
z =  get_zone(zonename)

def juned(zonename):
        #archive_dir is the direcory location defined in configuration
        zone_array = [f for f in os.listdir(archive_dir) if fnmatch.fnmatch(f,zonename+".*")]
        return zone_array


hostnames=['glam.com.']

data=juned(zonename)
#data=z.names.keys()
print data

soa_array = [ i.split(zonename,1)[1][1:] for i in data]
print soa_array
