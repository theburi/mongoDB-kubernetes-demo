kubectl create secret generic "adminopsmanager" --from-literal=Username="test@test.com" --from-literal=Password='<password>' --from-literal=FirstName="First" --from-literal=LastName="Last"

Open the Ops Manager application. In the UI, generate a new API key by selecting: “UserName -> Account -> Public API Access”

kubectl create secret generic om-jane-doe-credentials  --from-literal="user=<user.email>" --from-literal="publicApiKey=<private key>"

OM LDAP Admin Key: IKVIVVXX
OM LDAP Admin key: 34858168-307b-4df2-979b-bf5df9506215


OM  ADmin: VZKLHAXQ
2c466b6b-520f-42c1-a20c-c716fe5f7ccb
orgid: 5ed0f2e37a4e6b005b5b6388