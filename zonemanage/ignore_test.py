from zonemanage import *
from django.forms.formsets import formset_factory
from forms import RecordsForm
from django.conf import settings

SUPPORTED_RECORD_TYPES=['NS']

settings.configure()

zonename='glam.com'
z =  get_zone(zonename)

def revert(zone,archive):
        z = get_zone(zone)
        za = get_archive(zone, archive)
        archive_serial = za.root.soa.serial
        archive_file = archive_zone(z,'admin')

        za.root.soa.serial = z.root.soa.serial
        za.save(filename=z.filename, autoserial=True)

        msg=["Zone %s reverted back to serial %s"  %(zonename,archive_serial)]
        return msg


data=revert(zonename,'glam.com.2014052221-junedm')
print data
