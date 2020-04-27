import requests
from deepmerge import always_merger
from requests.auth import HTTPDigestAuth

getOMKey = '<key>'
getOMSECRET = '<secret>'
  

def getLdapConfigForOm():
  return {
    # Secret
    'bindQueryPassword' : 'password',
    'bindQueryUser'     : 'cn=admin,dc=ldap,dc=mongodb,dc=local',
    # ConfigMap
    'authzQueryTemplate' : '{USER}?memberOf?base',
    'servers'            : 'ec2-52-60-78-132.ca-central-1.compute.amazonaws.com:389',
    'userToDNMapping'    : '[ {  "ldapQuery": "ou=users,dc=ldap,dc=mongodb,dc=local??sub?(uid={0})", "match" : "(.+)" }  ]'  } 
#   if isEnabled(configParameter('LDAP_ENABLED')) else None

def getLDAPRoles():
    return [{
    'authenticationRestrictions' : [],
    'privileges'                 : [],
    'db'         : 'admin',
    'role'       : 'cn=admins,ou=groups,dc=ldap,dc=mongodb,dc=local',
    'roles'      : [
      {
        'db'   : 'admin',
        'role' : 'clusterAdmin'
      }, {
        'db'   : 'admin',
        'role' : 'dbAdminAnyDatabase'
      }, {
        'db'   : 'admin',
        'role' : 'readWriteAnyDatabase'
      }, {
        'db' : 'admin',
        'role': 'clusterMonitor'
      }
    ]
  }]
def enableAuthMechanismsForProject(groupId, ldapConfig, ldapRoles):
    def getAutomationConfig(group):
        """
        Returns the raw automation configuration object for an Ops Manager project.
        :param group: Project/Group ID of the Ops Manager project for which the data is being requested.
        """

        url = f'http://a55fbb5a2848f11eaaa090214ecb1cab-857889018.eu-west-1.elb.amazonaws.com:8080/api/public/v1.0/groups/{group}/automationConfig'
        print (url)
        OMKey = getOMKey()
        r = requests.get(url, auth=HTTPDigestAuth(getOMKey, getOMSECRET))
        print ("Getting Automation Config")
        print (r)
        return r.json()

    def putAutomationConfig(group, conf):
          print ('Removing External policy')
          policyurl = f'http://a55fbb5a2848f11eaaa090214ecb1cab-857889018.eu-west-1.elb.amazonaws.com:8080/api/public/v1.0/groups/{group}/controlledFeature'
          r_pol = requests.put(policyurl, headers={'Content-Type': 'application/json'}, auth=HTTPDigestAuth(getOMKey, getOMSECRET), json= {"policies": [],"externalManagementSystem": { "name": "Kubernetes Operator" }})
          print (r_pol.json())
          print ('Patching Automation config')
          url = f'http://a55fbb5a2848f11eaaa090214ecb1cab-857889018.eu-west-1.elb.amazonaws.com:8080/api/public/v1.0/groups/{group}/automationConfig'
          r = requests.put(url, headers={'Content-Type': 'application/json'}, auth=HTTPDigestAuth(getOMKey, getOMSECRET), json=conf)
          
          return r

    # Retrieve automation config
    conf = getAutomationConfig(groupId)
    # if conf.get('auth')['disabled']:
      # Authentication in OpsManager Project is not enabled yet, enabling it...
    key = 'alkdjlaksdjalksdjlaksjdlaksdjlkJLK234lkajsdlkajsldkajlkjsadasds'
    # initPwd = 'askldalkdjlasdjakjkle4askdjlvn'
    conf.get('auth')['disabled'] = False
    conf.get('auth')['authoritativeSet'] = True
    # conf.get('auth')['autoAuthMechanisms']        = ['SCRAM-SHA-256', 'MONGODB-CR']
    conf.get('auth')['autoAuthMechanisms'] = ['PLAIN']
    conf.get('auth')['deploymentAuthMechanisms'] = ['PLAIN']
    conf.get('auth')['keyfile'] = '/var/lib/mongodb-mms-automation/keyfile'
    conf.get('auth')[
        'keyfileWindows'] = '%SystemDrive%\\MMSAutomation\\versions\\keyfile'
    conf.get('auth')['autoUser'] = 'mms-automation-agent'
    # conf.get('auth')['autoPwd'] = 'password'
    conf.get('auth')['autoLdapGroupDN'] = 'cn=admins,ou=groups,dc=ldap,dc=mongodb,dc=local'
    conf.get('auth')['key'] = key

    conf['ldap'] = always_merger.merge({
        'validateLDAPServerConfig': True,
        'bindMethod': 'simple',
        'transportSecurity': 'none',
        'bindSaslMechanisms': ''
    }, ldapConfig)
    conf['roles'] = getLDAPRoles()
    # update the automation config
    #   print (conf)
    res = putAutomationConfig(groupId, conf)

    return res



result = enableAuthMechanismsForProject( '5ea0389510f39d007672a949', getLdapConfigForOm(), f'CN=MyLDAPGroup,DN=com')
print (result.json())
