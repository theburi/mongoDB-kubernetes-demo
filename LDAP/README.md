# MongoDB Kuberentes Operator and MongoDB LDAP configuration  
This section demonstrated process to configure LDAP for MongoDB Clusters deployed by Enterpise Operator

IMPORTANT: Only works with Kubernetes Operator v1.1 or v1.5.1+

1. Deploy MongoDB Cluster with Kubernetes Operator. Make sure 'spec.authentication' is not defined.
2. Take note of OpsManager project ID of newly deployed cluster
3. Run 'applyLDAP.py' script to apply LDAP confiuration

Script requires API Key to work. API Key can be optained from Ops Manager. 
* Navigate to a new project where new cluster has been deployed
* Access Manager-> (Tab) API Keys and Create new Key. Make sure Whitelist is correct.
* Define following environment variables

```    
    export OM_KEY=          
    export OM_SECRET=
    export OM_GROUPID=
    export OM_SERVER=     - OpsManager URL
```

Script 'applyLDAP.py' contains an example of a very specific LDAP configuration.
In order to change it please review following variables:

    'bindQueryPassword' : 'password',
    'bindQueryUser'     : 'cn=admin,dc=ldap,dc=mongodb,dc=local',
    'authzQueryTemplate' : '{USER}?memberOf?base',
    'servers'            : '<LDAP Server>:389',
    'userToDNMapping'    : '[ {  "ldapQuery": "ou=users,dc=ldap,dc=mongodb,dc=local??sub?(uid={0})", "match" : "(.+)" }  ]'  } 

    LDAP Roles `def getLDAPRoles():`


  "monitoringAgentTemplate": {
        "logRotate": {
            "sizeThresholdMB": 1000,
            "timeThresholdHrs": 24
        },
        "name": "7.2.0.488-1",
        "username": "agentuser",
        "ldapGroupDN": "cn=admins,ou=groups,dc=ldap,dc=mongodb,dc=local",
        "logPath": "/var/log/mongodb-mms-automation/monitoring-agent.log",
        "logPathWindows": "%SystemDrive%\\MMSAutomation\\log\\mongodb-mms-automation\\monitoring-agent.log"
    },
    "backupAgentTemplate": {
        "logRotate": {
            "sizeThresholdMB": 1000,
            "timeThresholdHrs": 24
        },
        "name": "7.8.1.1109-1",
        "username": "agentuser",
        "ldapGroupDN": "cn=admins,ou=groups,dc=ldap,dc=mongodb,dc=local",
        "logPath": "/var/log/mongodb-mms-automation/backup-agent.log",
        "logPathWindows": "%SystemDrive%\\MMSAutomation\\log\\mongodb-mms-automation\\backup-agent.log"
    },