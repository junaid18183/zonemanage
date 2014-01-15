# ** Application Config **

# zonedir : path to a directory containing all the zone files.
#   will read/write these files as changes are made.
zonedir = '/var/named/chroot/var/named/'

# rndc_path : path to the 'rndc' binary, which uses to signal
#   named to refresh a zone.  Leave as 'rndc' if it can be found in the
#   normal PATH.
#   Comment this option out if you want to disable refreshing of
#   zones by   Zones would need to be refreshed manually
#   or by some other means in this case.
rndc_path = '/usr/sbin/rndc'

#checkzone_path : path to the 'named-checkzone' binary, which uses to
#   verify that zone files are formatted correctly.  Leave as 'named-checkzone'
#   if it can be found in the normal PATH.
#   Comment this option out if you want to disable zone file verifications.
checkzone_path = '/usr/sbin/named-checkzone'

# archive_dir : directory to save old copies of zone files. These backup
#   files are accessible from the "change history" functionality of 
#   Comment this option out to disable saving backup copies.
archive_dir = '/var/tmp/zonemanage_archive/'

SUPPORTED_RECORD_TYPES = ('A', 'CNAME', 'MX', 'NS', 'TXT', 'PTR')
