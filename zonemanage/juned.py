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

#name="AbhishekT"
#basedn="DC=projecty,DC=com"
#import ldap
#server = 'ldap://10.0.1.3'
#user_dn = 'CN=jenkins,OU=service accounts,DC=projecty,DC=com'
#password = 'in$45Jun'
#con = ldap.initialize(server)
#con.simple_bind_s(user_dn, password)
#con.set_option(ldap.OPT_REFERRALS, 0)
#filter = "(&(objectClass=person)(sAMAccountName=name))"
#attrs = ['sn']
#results = con.search_s(basedn,ldap.SCOPE_SUBTREE,filter,attrs )
