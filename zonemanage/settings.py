# Django settings for zonemanage project.
import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(SITE_ROOT, 'db') + '/zonemanage.db', # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, "files")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/files/"
STATIC_URL= "/static/"
#Added By Juned

STATIC_ROOT = "/home/junedm/zonemanage/zonemanage/static/"

SECRET_KEY = 'iuo-zka8nnv0o+b*7#_*fcep$@f^35=)c#7_20z6i8g0oc&r!g'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'zonemanage.urls'

TEMPLATE_DIRS = (os.path.join(SITE_ROOT, "templates"),)
#STATICFILES_DIRS = ("/home/junedm/zonemanage/zonemanage/static/",)

LOGIN_URL="/zonemanage/login/"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'zonemanage',
)

########################################################################
#Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/zonemanage.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'zonemanage': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

########################################################################
# LDAP Authentication
########################################################################
import ldap,logging
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType ,ActiveDirectoryGroupType

logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
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


#AUTH_LDAP_USER_SEARCH = LDAPSearch("OU=Users,DC=projecty,DC=com", ldap.SCOPE_SUBTREE, "(CN=%(user)s)")
AUTH_LDAP_USER_SEARCH = LDAPSearch("DC=projecty,DC=com", ldap.SCOPE_SUBTREE, "(&(objectClass=person)(sAMAccountName=%(user)s))")
#AUTH_LDAP_GROUP_SEARCH = LDAPSearch("OU=Groups,DC=projecty,DC=com", ldap.SCOPE_SUBTREE, "(objectClass=group)")

# or perhaps:
#AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,OU=users,DC=projecty,DC=com"
#AUTH_LDAP_ALWAYS_UPDATE_USER = True

# set group type
AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType()

# Simple group restrictions
#~ AUTH_LDAP_REQUIRE_GROUP = "cn=enabled,OU=django,OU=groups,DC=example,DC=com"
#~ AUTH_LDAP_DENY_GROUP = "cn=disabled,OU=django,OU=groups,DC=example,DC=com"


# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
 "first_name": "givenName",
 "last_name": "sn",
 "email": "mail"
}

#~ AUTH_LDAP_PROFILE_ATTR_MAP = {
 #~ "employee_number": "employeeNumber"
#~ }


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
#'django.contrib.auth.backends.ModelBackend',
)

# End LDAP Authentication Settings
