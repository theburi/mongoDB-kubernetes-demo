import requests
from deepmerge import always_merger
from requests.auth import HTTPDigestAuth

def getLdapConfigForOm():
  return {
    # Secret
    'bindQueryPassword' : 'password',
    'bindQueryUser'     : 'cn=read-only-admin,dc=example,dc=com',
    # ConfigMap
    'authzQueryTemplate' : '{USER}?memberOf?base',
    'servers'            : 'ldap.forumsys.com',
    'userToDNMapping'    : '[ {  match : "(.+)", substitution: "uid={0},dc=example,dc=com"  }  ]'  } 
#   if isEnabled(configParameter('LDAP_ENABLED')) else None

def getLDAPRoles():
    return [{
    'authenticationRestrictions' : [],
    'privileges'                 : [],
    'db'         : 'admin',
    'role'       : f'CN=mathematicians,DN=com',
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
        r = requests.get(url, auth=HTTPDigestAuth('LNTMCKJX', 'e71aec97-903a-4d61-a9fa-ceb715dc8cc5'))
        print (r)
        return r.json()

    def putAutomationConfig(group, conf):
          policyurl = f'http://a55fbb5a2848f11eaaa090214ecb1cab-857889018.eu-west-1.elb.amazonaws.com:8080/api/public/v1.0/groups/{group}/controlledFeature'
          r_pol = requests.put(policyurl, headers={'Content-Type': 'application/json'}, auth=HTTPDigestAuth('LNTMCKJX', 'e71aec97-903a-4d61-a9fa-ceb715dc8cc5'), json= {"policies": [],"externalManagementSystem": { "name": "Kubernetes Operator" }})
          print (r_pol.json())
          url = f'http://a55fbb5a2848f11eaaa090214ecb1cab-857889018.eu-west-1.elb.amazonaws.com:8080/api/public/v1.0/groups/{group}/automationConfig'
          r = requests.put(url, headers={'Content-Type': 'application/json'}, auth=HTTPDigestAuth('LNTMCKJX', 'e71aec97-903a-4d61-a9fa-ceb715dc8cc5'), json=conf)
          return r

    # Retrieve automation config
    conf = getAutomationConfig(groupId)
    conf_old=conf
    if conf.get('auth')['disabled']:
      # Authentication in OpsManager Project is not enabled yet, enabling it...
      key     = 'alkdjlaksdjalksdjlaksjdlaksdjlkJLK234lkajsdlkajsldkajlkjsadasds'
      initPwd = 'askldalkdjlasdjakjkle4askdjlvn'
      conf.get('auth')['disabled']                 = False
      conf.get('auth')['authoritativeSet']         = True
      # conf.get('auth')['autoAuthMechanisms']        = ['SCRAM-SHA-256', 'MONGODB-CR']
      conf.get('auth')['autoAuthMechanisms']       = [ 'MONGODB-CR' ]
      conf.get('auth')['deploymentAuthMechanisms'] = [ 'PLAIN' ]
      conf.get('auth')['keyfile']                  = '/var/lib/mongodb-mms-automation/keyfile'
      conf.get('auth')['keyfileWindows']           = '%SystemDrive%\\MMSAutomation\\versions\\keyfile'
      conf.get('auth')['autoUser']    = 'riemann'
      conf.get('auth')['autoPwd']     = 'password'
      conf.get('auth')['key']         = key
      conf.get('auth')['usersWanted'] = [
        {
          'db'      : 'admin',
          'initPwd' : f'{initPwd}',
          'user'    : 'mms-monitoring-agent',
          'roles'   : [{ 'db': 'admin', 'role': 'clusterMonitor'}]
        }, {
          'db'      : 'admin',
          'initPwd' : f'{initPwd}',
          'user'    : 'mms-backup-agent',
          'roles'   : [
            { 'db': 'local', 'role': 'readWrite'},
            { 'db': 'admin', 'role': 'clusterAdmin'},
            { 'db': 'admin', 'role': 'readAnyDatabase'},
            { 'db': 'admin', 'role': 'userAdminAnyDatabase'}
          ]
        }
      ]
      conf['ldap'] = always_merger.merge({
          'validateLDAPServerConfig' : True,
          'bindMethod'               : 'simple',
          'transportSecurity'        : 'tls',
          'bindSaslMechanisms'       : ''
      }, ldapConfig)
      conf['roles'] = getLDAPRoles()
      # update the automation config
      #   print (conf)
      res = putAutomationConfig(groupId, conf)

      return res



result = enableAuthMechanismsForProject( '5ea0389510f39d007672a949', getLdapConfigForOm(), f'CN=MyLDAPGroup,DN=com')
print (result.json())