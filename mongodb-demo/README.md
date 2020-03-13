* This document explains how to deploy MongoDB cluster in Kubernetes

** Prerequesites:
- OpsManager has been configured and installed. Please follow instruction in ```opsmanager``` folder an note external url.
- Create new OpsManager organization and get org ID
- Create API key for this new organization as Org Owner (for this example) and make a note of it
    It should look like key: ETFBXKUH and private Key: 20b3bab8-10d8-4de0-9db5-529569dc053e
    add whitelist to the IP range of your Kubernetes cluster.  for example: 195.1.0.0/16

** Create Namespace `project1` where we are going to deploy MongoDB clusters.
It is a good practice to keep namespaces small and focused.
```
    kubectl apply -f mongodb-demo/nsProject1.yml 
    kubectl config set-context <name of kubectl context> --namespace=project1
```

** Create MongoDB Enterprise Operator
We need to deploy Operator into each namespace where we need to run MongoDB Clusters. 
However OpsManager will be shared between all MogoDB clusters/Operator in your organization, globally.

```
    kubectl apply -f mongodb-demo/mongodb-enterprise.yaml
```

** Create Secrete to store Ops Manager APi Key
this secrete could be used for all MongoDB clusters deployed in this namespace. 
```
kubectl create secret generic opsmanager-org-access-key  --from-literal="user=ETFBXKUH" --from-literal="publicApiKey=20b3bab8-10d8-4de0-9db5-529569dc053e"
```
** Create config map `demo-cluster-1` for our first MongoDB Cluster

Add OrgID created at the beginning of this tutorial to mongodb-demo/demo-cluseter-1.yaml. If OrgID is ommoted, Operator will try to create new Org. API Key that was created previously does not have permission to create Organization.

Try OpsManager CLI to automate OpsManager common tasks https://github.com/mongodb/mongocli

Change baseURL to the url of Ops Manager. Don't forget to include port if different to 80.

```
    kubectl apply -f mongodb-demo/demo-cluster-1.yaml
```
Do not reuse config maps for different MongoDB Clusters! Alwasy have 1:1 mapping. 

** Create MongoDB Cluster

MongoDB cluster we are going to deploy in this demo is not sutable for production. We removed security configuration to simplify this example. TLS and Authentication must be anabled for any production environment. Luckly Operator will do majority of heavy lifting for you and would make a secue cluster configuration a breeze. 

```
    kubectl apply -f mongodb-demo/demo-mongodb-cluster-1.yaml
```

In a few seconds we should see first Statefull set been created

``` kubectl get pods ```

demo-mongodb-cluster-1-0  0/1     ContainerCreating   0          21s

if that is not happening please check Operator logs for more information
