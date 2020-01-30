kubectl create secret generic "adminopsmanager" --from-literal=Username="test@test.com" --from-literal=Password='KubeTest12!' --from-literal=FirstName="First" --from-literal=LastName="Last"

kubectl create secret generic om-jane-doe-credentials  --from-literal="user=DCIGYXYQ" --from-literal="publicApiKey=4ab3b876-2349-4bc0-93f0-3302bc4ae7d5"