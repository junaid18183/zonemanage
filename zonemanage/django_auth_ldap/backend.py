import ldap;

from django.contrib.auth.models import User, Group

class ActiveDirectoryGroupMembershipSSLBackend:
    #Required parameters
    AD_DNS_NAME ='your remote ldap server location';
    AD_LDAP_PORT = 636
    AD_LDAP_URL = 'ldaps://%s' % AD_DNS_NAME;
    AD_SEARCH_DN = 'dc=bbc,dc=ad,dc=bcc,dc=net'; # this is your search dn
    AD_NT4_DOMAIN = 'bbc.ad.bbc.net'; #its your ad domain
    AD_SEARCH_FIELDS = ['mail','givenName','sn','sAMAccountName','memberOf'];
    AD_MEMBERSHIP_REQ = ['Group_Required','Alternative_Group'];
    AD_CERT_FILE = "C:/player/Python/Application/cert/mycert.cer";
AD_DEBUG = False;
AD_DEBUG_FILE ='';

def authenticate(self,username=None,password=None):
    try:
        if len(password) == 0:
            return None
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
        ldap.set_option(ldap.OPT_NETWORK_TIMEOUT, 2)
        l = ldap.initialize(self.AD_LDAP_URL)
        l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        binddn = "%s@%s" % (username,self.AD_NT4_DOMAIN)
        l.simple_bind_s(binddn,password)
        l.unbind_s()
        return self.get_or_create_user(username,password)

    except ImportError:
        pass
    except ldap.INVALID_CREDENTIALS:
        pass

def get_or_create_user(self, username, password):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:

        try:
        # debug info
            debug=0
            if len(self.AD_DEBUG_FILE) > 0:
                if self.AD_DEBUG:
                    debug = open(self.AD_DEBUG_FILE,'w')
                    print >>debug, "create user %s" % username

            ldap.set_option(ldap.OPT_X_TLS_CACERTFILE,self.AD_CERT_FILE)
            ldap.set_option(ldap.OPT_REFERRALS,0) # DO NOT TURN THIS OFF OR SEARCH WON'T WORK!      
            # initialize
            if debug:
                print >>debug, 'ldap.initialize...'
            l = ldap.initialize(self.AD_LDAP_URL)
            l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)

            # bind
            if debug:
                print >>debug, 'bind...'
            binddn = "%s@%s" % (username,self.AD_NT4_DOMAIN)
            l.bind_s(binddn,password)

            # search
            if debug:
                print >>debug, 'search...'
            result = l.search_ext_s(self.AD_SEARCH_DN,ldap.SCOPE_SUBTREE,"sAMAccountName=%s" % username,self.AD_SEARCH_FIELDS)[0][1]
            if debug:
                print >>debug, result

            # Validate that they are a member of review board group
            if result.has_key('memberOf'):
                membership = result['memberOf']
            else:
                membership = None
            if debug:
                print >>debug, "required:%s" % self.AD_MEMBERSHIP_REQ
            bValid=0
            for req_group in self.AD_MEMBERSHIP_REQ:
                if debug:
                    print >>debug, "Check for %s group..." % req_group
                for group in membership:
                    group_str="CN=%s," % req_group
                    if group.find(group_str) >= 0:
                        if debug:
                            print >>debug, "User authorized: group_str membership found!"
                        bValid=1
                        break
            if bValid == 0:
                if debug:
                    print >>debug, "User not authorized, correct group membership not found!"
                return None

            # get email
            if result.has_key('mail'):
                mail = result['mail'][0]
            else:
                mail = None
            if debug:
                print >>debug, "mail=%s" % mail
            # get surname
            if result.has_key('sn'):
                last_name = result['sn'][0]
            else:
                last_name = None
            if debug:
                print >>debug, "sn=%s" % last_name

            # get display name
            if result.has_key('givenName'):
                first_name = result['givenName'][0]
            else:
                first_name = None
            if debug:
                print >>debug, "first_name=%s" % first_name

            l.unbind_s()

            user = User(username=username,first_name=first_name,last_name=last_name,email=mail)

        except Exception, e:
            if debug:
                print >>debug, "exception caught!"
                print >>debug, e
            return None

        user.is_staff = False
        user.is_superuser = False
        user.set_password('ldap authenticated')
        user.save()

        # add user to default group
        group=Group.objects.get(pk=1)
        if debug:
            print >>debug, group
        if debug:
            print >>debug, "add %s to group %s" % (username,group)
        user.groups.add(group)
        user.save()
        if debug:
            print >>debug, "successful group add"

        if debug:
            debug.close()

    return user

def get_user(self, user_id):
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None
