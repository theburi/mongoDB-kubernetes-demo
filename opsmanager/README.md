Deploy Ops Manager in Kuberentes with MongoDB Enterprise Operator
These instructions cover Ops Manager configuration in Local Mode. For Kubernetes cluster that are isolated from Internet.

* Installation instructions 
** Cleanup Demo environment

bash opsmanager/cleanup.sh

** Apply secrets for Ops manager access credential.
kubectl create secret generic "adminopsmanager" --from-literal=Username="test@test.com" --from-literal=Password='KubeTest12!' --from-literal=FirstName="First" --from-literal=LastName="Last"

** Create Persistent volumes Claim

Ops Manager will hold MongoDB installers on a local disk. We need to create Persistent volume to keep this volume betwwwen pod restarts.

```
$ kubectl apply -f opsmanager/packages-pvc.yaml
```
note: `opsmanager-packages-claim` PVC must get Bound to a PV. 
To check run `kubectl get pvc` and ensure that PVC has the following status
`opsmanager-packages-claim   Bound pvc-737c0892-58a3-11ea-acf5-06d23bd67f40   10Gi       RWO`
In some cases a new storage class with Immidiate provisioning could help to fulfill pvc.
We included a sample of storage class opsmanager/packages-sc.yaml

** Generate Ops Manager API Key and create new secret. Operator needs API Keys to authenticate with Ops Manager and configure clusters.

https://docs.opsmanager.mongodb.com/current/tutorial/manage-agent-api-key/

kubectl create secret generic backup-credentials  --from-literal="user=<key or email>" --from-literal="publicApiKey=<private key>"

** Launch Ops Manager without Backup

```
kubectl apply -f opsmanager/ops-manager.yaml 
```
In few minutes opsmanager will get into Running state and will be accesible over external-ip service endpoint.

```
kubectl get svc ops-manager-svc-ext
```

** Copy file needed to launch clusters in Local Mode

In this example we will use MongoDB 4.2.0
```
wget https://downloads.mongodb.com/linux/mongodb-linux-x86_64-enterprise-ubuntu1604-4.2.0.tgz
```

```
kubectl cp mongodb-linux-x86_64-enterprise-ubuntu1604-4.2.0.tgz ops-manager-0:/mongodb-ops-manager/mongodb-releases/mongodb-linux-x86_64-enterprise-ubuntu1604-4.2.0.tgz
```
** Apply Backup S3 bucket keys
```
kubectl create secret generic s3-credentials   --from-literal=accessKey="<key goes here>" --from-literal=secretKey="<AWS Token>"
```
** Create DataBases needed for Backup infrastructure
```
kubectl apply opsmanager/backup-db.yaml
```
** Apply new OpsManager configuration to include new  Backup infrastructure
```
kubectl apply -f opsmanager/ops-manager-backup.yaml
```

** Configure Container Register that requires authentication 

First step. lets create Secrete that will hold credentials for container registry

```
kubectl create secret docker-registry regcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
```

There are two methods to configure auth of container registry

1. Add this secrete to each Resource PodSpecTemplate
spec:
    podSpec:
        podTemplate:
            imagePullSecret:
              - name: regcred

2. Add this secrete to a Service account. 
if the pod does not contain any ``ImagePullSecrets``, then ``ImagePullSecrets`` of the ``ServiceAccount`` are added to the pod.
https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#add-imagepullsecrets-to-a-service-account

for OpsManager we use two service accounts: mongodb-enterprise-appdb and mongodb-enterprise-database-pods

```
imagePullSecret:
    - name: regcred
  ```