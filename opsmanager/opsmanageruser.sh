kubectl create secret generic "adminopsmanager" --from-literal=Username="test@test.com" --from-literal=Password='<password>' --from-literal=FirstName="First" --from-literal=LastName="Last"

Open the Ops Manager application. In the UI, generate a new API key by selecting: “UserName -> Account -> Public API Access”

kubectl create secret generic om-jane-doe-credentials  --from-literal="user=<user.email>" --from-literal="publicApiKey=<private key>"