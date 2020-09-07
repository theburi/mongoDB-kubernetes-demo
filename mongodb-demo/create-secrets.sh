


# First Member Certificate
kubectl get secret/demo-mongodb-cluster-1-0 -o jsonpath='{.data.tls\.crt}' | base64 --decode > demo-mongodb-cluster-1-0-pem
kubectl get secret/demo-mongodb-cluster-1-0 -o jsonpath='{.data.tls\.key}' | base64 --decode >> demo-mongodb-cluster-1-0-pem

# Second Member Certificate
kubectl get secret/demo-mongodb-cluster-1-1 -o jsonpath='{.data.tls\.crt}' | base64 --decode > demo-mongodb-cluster-1-1-pem
kubectl get secret/demo-mongodb-cluster-1-1 -o jsonpath='{.data.tls\.key}' | base64 --decode >> demo-mongodb-cluster-1-1-pem

# Third Member Certificate
kubectl get secret/demo-mongodb-cluster-1-2 -o jsonpath='{.data.tls\.crt}' | base64 --decode > demo-mongodb-cluster-1-2-pem
kubectl get secret/demo-mongodb-cluster-1-2 -o jsonpath='{.data.tls\.key}' | base64 --decode >> demo-mongodb-cluster-1-2-pem

kubectl delete secret demo-mongodb-cluster-1-cert
kubectl create secret generic demo-mongodb-cluster-1-cert --from-file=demo-mongodb-cluster-1-0-pem --from-file=demo-mongodb-cluster-1-1-pem --from-file=demo-mongodb-cluster-1-2-pem

rm demo-mongodb-cluster-1-*

# Generating CA Secret

cat ../ca/ca.crt > ca-pem
kubectl delete cm ca-db1
kubectl create configmap ca-db1 --from-file=ca-pem

cat ../ca/ca.crt > mms-ca.crt
kubectl create configmap ca-om --from-file=mms-ca.crt
