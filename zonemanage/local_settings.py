########################################################################
import logging


#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'formatters': {
#        'verbose': {
#            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#            'datefmt' : "%d/%b/%Y %H:%M:%S"
#        },
#        'simple': {
#            'format': '%(levelname)s %(message)s'
#        },
#    },
#    'handlers': {
#        'file': {
#            'level': 'DEBUG',
#            'class': 'logging.FileHandler',
#            'filename': '/var/log/zonemanage.log',
#            'formatter': 'verbose'
#        },
#    },
#    'loggers': {
#        'django': {
#            'handlers':['file'],
#            'propagate': True,
#            'level':'DEBUG',
#        },
#        'zonemanage': {
#            'handlers': ['file'],
#            'level': 'DEBUG',
#        },
#    }
#}

########################################################################
# LDAP Authentication
########################################################################
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType ,ActiveDirectoryGroupType

logger = logging.getLogger('django_auth_ldap')
#logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.FileHandler('/var/log/zonemanage.log'))
logger.setLevel(logging.DEBUG)


#AUTH_LDAP_START_TLS = True
AUTH_LDAP_GLOBAL_OPTIONS = {
 ldap.OPT_X_TLS_REQUIRE_CERT: False,
 ldap.OPT_REFERRALS: False,
}

# Baseline configuration.
AUTH_LDAP_SERVER_URI = "ldap://10.0.1.3"
AUTH_LDAP_BIND_DN = "CN=jenkins,OU=service accounts,DC=projecty,DC=com"
AUTH_LDAP_BIND_PASSWORD = "in$45Jun"


AUTH_LDAP_USER_SEARCH = LDAPSearch("DC=projecty,DC=com", ldap.SCOPE_SUBTREE, "(&(objectClass=person)(sAMAccountName=%(user)s))")
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("DC=projecty,DC=com", ldap.SCOPE_SUBTREE, "(&(objectClass=group))")

# or perhaps:
#AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,OU=users,DC=projecty,DC=com"
#AUTH_LDAP_ALWAYS_UPDATE_USER = True

# set group type
AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType()

#Simple group restrictions
AUTH_LDAP_REQUIRE_GROUP = "CN=techops1,OU=Distribution Groups,DC=projecty,DC=com"
#AUTH_LDAP_DENY_GROUP = "cn=disabled,OU=django,OU=groups,DC=example,DC=com"


# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
 "first_name": "givenName",
 "last_name": "sn",
 "email": "mail"
}

AUTH_LDAP_PROFILE_ATTR_MAP = {
 "first_name": "givenName",
 "last_name": "sn",
 "email": "mail"
}


#AUTH_LDAP_USER_FLAGS_BY_GROUP = {
# "is_active": "cn=active,OU=Groups,DC=parent,DC=ssischool,DC=org",
# "is_staff": "cn=staff,OU=Groups,DC=parent,DC=ssischool,DC=org",
# "is_superuser": "cn=superuser,OU=Groups,DC=parent,DC=ssischool,DC=org"
#}

#~ AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = {
 #~ "is_awesome": "cn=awesome,OU=django,OU=groups,DC=example,DC=com",
#~ }


# important! to use the group's permission
#AUTH_LDAP_MIRROR_GROUPS = True


# Use LDAP group membership to calculate group permissions.
#AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache group memberships for an hour to minimize LDAP traffic
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 2


# !important# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
'django_auth_ldap.backend.LDAPBackend',
'django.contrib.auth.backends.ModelBackend',
)

# End LDAP Authentication Settings

