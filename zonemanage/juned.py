#! /usr/bin/python 
from zonemanage import *

zonename='glam.colo'
zonefile='/var/named/chroot/var/named/glam.colo'
#print zonename,zonefile 
#status=check_zone(zonename, zonefile)
#z=get_zone(zonename)
#status=archive_zone(z)

#status=get_archive(zonename, 'glam.colo.2014010700')
#print status.root.soa.serial
#soa_fields={'rname': u'root.1.143.10.in-addr.arpa.', 'retry': 900, 'mname': u'localhost.1.143.10.in-addr.arpa.', 'refresh': 10800, 'expire': 604800, 'serial': 2015112216, 'minttl': 86400}

#status=savesoa('1.143.10.in-addr.arpa',soa_fields)

#status=reload('1.143.10.in-addr.arpa')
#print status


#z=get_zone(zonename)
#hostnames = sorted_hostnames(zonename, z.names.keys())
#zone_data=dns_records(z,hostnames)
#types=SUPPORTED_RECORD_TYPES
#print zone_data['zones']
