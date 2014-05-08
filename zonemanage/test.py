from zonemanage import *
from django.forms.formsets import formset_factory
from forms import RecordsForm
from django.conf import settings

SUPPORTED_RECORD_TYPES=['NS']

settings.configure()

zonename='glam.com'
z =  get_zone(zonename)


def juned(z,hostnames):
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


hostnames=['glam.com.']

data=juned(z,hostnames)
#data=z.names.keys()
print data
