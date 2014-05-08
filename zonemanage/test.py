from zonemanage import *
from django.forms.formsets import formset_factory
from forms import RecordsForm
from django.conf import settings

settings.configure()

#RecordsFormset = formset_factory(RecordsForm,extra=0)
#formset = RecordsFormset()
#formset = RecordsFormset(initial=[{"hostname" : "Juned","type" : "A" , "value":"192.168.3.10" , 'preference':'100'}])

#print formset.errors

#print "is Formset Valid", formset.valid()

#for form in formset:
#	print "form is", form
#	print "is form valid?",form.is_valid()
#	print "form error " , form.errors
#	#print "form cleaned data" ,form.cleaned_data

#for form in formset.forms:
#	if form.is_valid():
#		print(form.cleaned_data)
#	else:
#		print "Juned"
#		print form.errors

z_records=[{'hostname': u'ggvaapp07.glam.com.', 'type': u'A', 'preference': u'', 'value': u'10.143.2.27'},{'hostname': u'ggvaapp07vm1.glam.com.', 'type': u'A', 'preference': u'', 'value': u'10.143.3.24'},{'hostname': u'ggvaapp07vm2.glam.com.', 'type': u'A', 'preference': u'', 'value': u'10.143.3.25'},{'hostname': u'ggvaapp07vm3.glam.com.', 'type': u'A', 'preference': u'', 'value': u'10.143.3.26'},{'hostname': u'ggvaapp07vm4.glam.com.', 'type': u'A', 'preference': u'', 'value': u'10.143.3.27'},{'hostname': u'glam.com.', 'type': u'NS', 'preference': u'', 'value': u'ggvaapp07.glam.com.'}]
zonename='glam.com'

z = get_zone(zonename)
save_ok = True
auto_inc_serial = False
names = z.names.keys()
names.remove(z.domain)  # remove '@' (root)
for name in names:
                z.delete_name(name)
                # delete nodes from '@' but don't remove it completely (otherwise SOA is gone...)
                root = z.root
                root.clear_all_records(exclude='SOA')
#print z.names.keys()				
for record in z_records:
	hostname = record['hostname']
        rtype = record['type']
       	preference = record['preference']
        value = record['value']
	if hostname and value and rtype:
		#if hostname not in z.names.keys():
		 if save_ok : ## Just for test
			z.add_name(hostname)
			name = z.names[hostname]
                        if rtype == 'MX':
	                        name.records(rtype, create=True).add( (int(preference), str(value)) )
				print hostname,rtype,preference,value
				print"------------"
                        else:
				name.records(rtype, create=True).add(str(value))
				print hostname,rtype,preference,value
				print"------------"

z.save()
print z.names.keys()
