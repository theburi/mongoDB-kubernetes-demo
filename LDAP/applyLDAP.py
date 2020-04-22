def getLdapConfigForOm():
  return {
    # Secret
    'bindQueryPassword' : configParameter('queryPassword'),
    'bindQueryUser'     : configParameter('queryUser'),
    # ConfigMap
    'authzQueryTemplate' : configParameter('LDAP_QUERY_TEMPLATE'),
    'servers'            : configParameter('LDAP_SERVERS'),
    'userToDNMapping'    : configParameter('LDAP_USERS_TO_DN_MAPPING')
  } if isEnabled(configParameter('LDAP_ENABLED')) else None

def enableAuthMechanismsForProject(self, groupId, ldapConfig, ldapRoles, backupConfig):
    # Retrieve automation config
    conf = self.getAutomationConfig(groupId)
    if conf.get('auth')['disabled']:
      # Authentication in OpsManager Project is not enabled yet, enabling it...
      key     = getRandomBase64Key(756)
      initPwd = getRandomBase64Key(20)
      conf.get('auth')['disabled']                 = False
      conf.get('auth')['authoritativeSet']         = True
      # conf.get('auth')['autoAuthMechanisms']        = ['SCRAM-SHA-256', 'MONGODB-CR']
      conf.get('auth')['autoAuthMechanisms']       = [ 'MONGODB-CR' ]
      conf.get('auth')['deploymentAuthMechanisms'] = [ 'MONGODB-CR' ]
      conf.get('auth')['keyfile']                  = '/var/lib/mongodb-mms-automation/keyfile'
      conf.get('auth')['keyfileWindows']           = '%SystemDrive%\\MMSAutomation\\versions\\keyfile'
      conf.get('auth')['autoUser']    = 'mms-automation'
      conf.get('auth')['autoPwd']     = f'{initPwd}'
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
      if ldapConfig is not None:
        conf.get('auth')['deploymentAuthMechanisms'].append('PLAIN')
        conf['ldap'] = always_merger.merge({
          'validateLDAPServerConfig' : True,
          'bindMethod'               : 'simple',
          'transportSecurity'        : 'tls',
          'bindSaslMechanisms'       : ''
        }, ldapConfig)
        conf['roles'] = ldapRoles
      # update the automation config
      return self.putAutomationConfig(groupId, conf)

      def getAutomationConfig(self, group):
        """
        Returns the raw automation configuration object for an Ops Manager project.
        :param group: Project/Group ID of the Ops Manager project for which the data is being requested.
        """
        return self.__get(f"/groups/{group}/automationConfig").json()