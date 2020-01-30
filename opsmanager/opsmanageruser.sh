kubectl create secret generic "adminopsmanager" --from-literal=Username="test@test.com" --from-literal=Password='<password>' --from-literal=FirstName="First" --from-literal=LastName="Last"

kubectl create secret generic om-jane-doe-credentials  --from-literal="user=<public key>" --from-literal="publicApiKey=<private key>"