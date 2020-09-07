How to create certs required for Ops Manager Secure configuration

1. isntall cert manager https://cert-manager.io/docs/installation/
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v0.16.0/cert-manager.yaml
2. create issuer
# Generate a CA private key
$ openssl genrsa -out ca.key 2048

# Create a self signed Certificate, valid for 10yrs with the 'signing' option set
$ openssl req -x509 -new -nodes -key ca.key -subj "/CN=${COMMON_NAME}" -days 3650 -reqexts v3_req -extensions v3_ca -out ca.crt


3. 'kubectl apply -f OpsManager-certs.yaml'

4. Concatenate all of them into right files and secretes
``
# First Member Certificate
kubectl -n mongodb get secret/ops-manager-db-0 -o jsonpath=’{.data.tls\.crt}’ | base64 --decode > ops-manager-db-0-pem
kubectl -n mongodb get secret/ops-manager-db-0 \
  -o jsonpath=’{.data.tls\.key}’ | base64 --decode >> ops-manager-db-0-pem

# Second Member Certificate
kubectl -n mongodb get secret/ops-manager-db-1 \
  -o jsonpath=’{.data.tls\.crt}’ | base64 --decode > ops-manager-db-1-pem
kubectl -n mongodb get secret/ops-manager-db-1 \
  -o jsonpath=’{.data,tls\.key}’ | base64 --decode >> ops-manager-db-1-pem

# Third Member Certificate
kubectl -n mongodb get secret/ops-manager-db-2 \
  -o jsonpath=’{.data.tls\.crt}’ | base64 --decode > ops-manager-db-2-pem
kubectl -n mongodb get secret/ops-manager-db-2 \
  -o jsonpath=’{.data.tls\.key}’ | base64 --decode >> ops-manager-db-2-pem
``