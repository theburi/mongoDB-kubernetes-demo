import requests
from deepmerge import always_merger
from requests.auth import HTTPDigestAuth
import os

import random
import string

getOMKey = os.getenv('OM_KEY')
getOMSECRET = os.getenv('OM_SECRET')
OMGroupID = os.getenv('OM_GROUPID')
OMServer =   os.getenv('OM_SERVER')



def randomString(stringLength=96):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))


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
      }, {
        'db': 'admin',
        'role': 'userAdminAnyDatabase'
      }
    ]
  }]
def enableAuthMechanismsForProject(groupId, ldapConfig, ldapRoles):
    def getAutomationConfig(group):
        """
        Returns the raw automation configuration object for an Ops Manager project.
        :param group: Project/Group ID of the Ops Manager project for which the data is being requested.
        """

        url = f'{OMServer}/api/public/v1.0/groups/{group}/automationConfig'
        print (url)
        r = requests.get(url, auth=HTTPDigestAuth(getOMKey, getOMSECRET))
        print ("Getting Automation Config")
        # print (r.json())
        return r.json()

    def getMonitoringConfig(group):
        """
        Returns the raw automation configuration object for an Ops Manager project.
        :param group: Project/Group ID of the Ops Manager project for which the data is being requested.
        """

        url = f'{OMServer}/api/public/v1.0/groups/{group}/automationConfig/monitoringAgentConfig'
        print (url)
        r = requests.get(url, auth=HTTPDigestAuth(getOMKey, getOMSECRET))
        print ("Getting Monitoring Config")
        # print (r.json())
        return r.json()

    def getBackupConfig(group):
        """
        Returns the raw automation configuration object for an Ops Manager project.
        :param group: Project/Group ID of the Ops Manager project for which the data is being requested.
        """

        url = f'{OMServer}/api/public/v1.0/groups/{group}/automationConfig/backupAgentConfig'
        print (url)
        r = requests.get(url, auth=HTTPDigestAuth(getOMKey, getOMSECRET))
        print ("Getting Backup Config")
        # print (r.json())
        return r.json()

    def putAutomationConfig(group, conf):
          print ('Removing External policy')
          policyurl = f'{OMServer}/api/public/v1.0/groups/{group}/controlledFeature'
          r_pol = requests.put(policyurl, headers={'Content-Type': 'application/json'}, auth=HTTPDigestAuth(getOMKey, getOMSECRET), json= {"policies": [],"externalManagementSystem": { "name": "Kubernetes Operator" }})

          print ('Patching Automation config')
          url = f'{OMServer}/api/public/v1.0/groups/{group}/automationConfig'
          r = requests.put(url, headers={'Content-Type': 'application/json'}, auth=HTTPDigestAuth(getOMKey, getOMSECRET), json=conf)
          
          return r

    def putMonitoringConfig(group, conf):
          print ('Removing External policy')
          policyurl = f'{OMServer}/api/public/v1.0/groups/{group}/controlledFeature'
          r_pol = requests.put(policyurl, headers={'Content-Type': 'application/json'}, auth=HTTPDigestAuth(getOMKey, getOMSECRET), json= {"policies": [],"externalManagementSystem": { "name": "Kubernetes Operator" }})

          print ('Patching Monitoring config')
          url = f'{OMServer}/api/public/v1.0/groups/{group}/automationConfig/monitoringAgentConfig'
          r = requests.put(url, headers={'Content-Type': 'application/json'}, auth=HTTPDigestAuth(getOMKey, getOMSECRET), json=conf)
          
          return r

    def putBackupConfig(group, conf):
          print ('Removing External policy')
          policyurl = f'{OMServer}/api/public/v1.0/groups/{group}/controlledFeature'
          r_pol = requests.put(policyurl, headers={'Content-Type': 'application/json'}, auth=HTTPDigestAuth(getOMKey, getOMSECRET), json= {"policies": [],"externalManagementSystem": { "name": "Kubernetes Operator" }})

          print ('Patching Backup config')
          url = f'{OMServer}/api/public/v1.0/groups/{group}/automationConfig/backupAgentConfig'
          r = requests.put(url, headers={'Content-Type': 'application/json'}, auth=HTTPDigestAuth(getOMKey, getOMSECRET), json=conf)
          
          return r

    # Retrieve automation config
    conf = getAutomationConfig(groupId)

      # Authentication in OpsManager Project is not enabled yet, enabling it...
    key = randomString()
    # initPwd = 'askldalkdjlasdjakjkle4askdjlvn'
    conf.get('auth')['disabled'] = False
    conf.get('auth')['authoritativeSet'] = True
    # conf.get('auth')['autoAuthMechanisms']        = ['SCRAM-SHA-256', 'MONGODB-CR']
    conf.get('auth')['autoAuthMechanisms'] = ['PLAIN']
    conf.get('auth')['deploymentAuthMechanisms'] = ['PLAIN']
    conf.get('auth')['keyfile'] = '/var/lib/mongodb-mms-automation/keyfile'
    conf.get('auth')['keyfileWindows'] = '%SystemDrive%\\MMSAutomation\\versions\\keyfile'
    conf.get('auth')['autoUser'] = 'agentuser'
    conf.get('auth')['autoPwd'] = 'password'
    conf.get('auth')['autoLdapGroupDN'] = 'cn=admins,ou=groups,dc=ldap,dc=mongodb,dc=local'
    # conf.get('auth')['key'] = key

    conf['ldap'] = always_merger.merge({
        'validateLDAPServerConfig': True,
        'bindMethod': 'simple',
        'transportSecurity': 'none',
        'bindSaslMechanisms': ''
    }, ldapConfig)
    conf['roles'] = getLDAPRoles()
    # update the automation config
   
    res = putAutomationConfig(groupId, conf)

    # Monitoring config
    Monitoringconf = getMonitoringConfig(groupId)
    print (Monitoringconf)
    Monitoringconf['username'] = 'jane'
    Monitoringconf['ldapGroupDN'] = 'cn=admins,ou=groups,dc=ldap,dc=mongodb,dc=local'
    Monitoringconf['password'] = 'password'
    res = putMonitoringConfig(groupId, Monitoringconf)

    # Backup config
    Backupconf = getBackupConfig(groupId)
    print (Backupconf)
    Backupconf['username'] = 'jane'
    Backupconf['ldapGroupDN'] = 'cn=admins,ou=groups,dc=ldap,dc=mongodb,dc=local'
    Backupconf['password'] = 'password'
    res = putBackupConfig(groupId, Backupconf)
   
    # conf['monitoringAgentTemplate']['username'] = 'mms-automation-agent'
    # conf.get('monitoringAgentTemplate')['autoLdapGroupDN'] = 'cn=admins,ou=groups,dc=ldap,dc=mongodb,dc=local'




    return res



result = enableAuthMechanismsForProject( OMGroupID, getLdapConfigForOm(), f'CN=MyLDAPGroup,DN=com')
print (result.json())
