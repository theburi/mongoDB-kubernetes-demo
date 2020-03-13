
# MongoDB Enterprise Operator Demo project

This is a Demo project that can help to quickly start with MongoDB on Kubernetes Platform. Samples used in this projects are used in my Presentations and Webinars. In this demo will cover MongoDB Enterpise toolset.

Version of Operator used int his Demo is 1.4.x

There are three parts

1. Install CRD and start Operator
2. Install and configure MongoDB Ops Manager
3. Start first MongoDB cluster


For this demo we will be using local Kubernetes cluster, however any Kubernetes cluster will work. Don't forget to set the right kubectl context. In this case it called `docker-desktop`

1. Install CRD and start Operator
   
MongoDB Operator repository https://github.com/mongodb/mongodb-enterprise-kubernetes is added as a submodule to this project.
It contains CRD and Operator yaml that we will use in this demo. 

   - Lets install CRD into our Kubernetes cluster. This command requires Admin permission.
```bash
cd mongodb-enterprise-kubernetes
kubectl apply -f crds.yaml
```

3 New Resource Defeinitons has been added to Kubernetes. However there are not controllers in Kuberenetes that manager them. This is where MongoDB Operator comes in. 
customresourcedefinition.apiextensions.k8s.io/mongodb.mongodb.com 
customresourcedefinition.apiextensions.k8s.io/mongodbusers.mongodb.com 
customresourcedefinition.apiextensions.k8s.io/opsmanagers.mongodb.com
clusterrole.rbac.authorization.k8s.io/mongodb-enterprise-operator-mongodb-webhook

   - Deploy Operator
   First we need to provision namespace `mongodb`, we will use this namespace for our MongoDB Clusters in this example. Note that our active context is `docker-desktop` and we will add namespace `mongodb` as a default namespace.
   if you wish to use different namespace, don't forget to change it in mongodb-enterprise-kubernetes/mongodb-enterprise.yaml
   ```bash
   cd ..
   kubectl apply -f namespace.yml
   kubectl config set-context docker-desktop --namespace=mongodb
   ```

   Now we are ready to deploy our operator.
   ```bash
   cd mongodb-enterprise-kubernetes
   kubectl apply -f mongodb-enterprise.yaml
   ```

   After a few seconds we could check that operator is running
   ```bash
   kubectl describe deployments mongodb-enterprise-operator
   ```
   Quick check that everything is in order.
   * Image:      quay.io/mongodb/mongodb-enterprise-operator:1.4.1
   * Replicas:   1 desired | 1 updated | 1 total | 1 available | 0 unavailable

2. Install and configure MongoDB Ops Manager

Note: For OpsManager configuration in "Local" mode, check our ./opsmanager directory

** Apply secrets for Ops manager
```bash
kubectl create secret generic "adminopsmanager" --from-literal=Username="<test@test.com>" --from-literal=Password='<password>' --from-literal=FirstName="First" --from-literal=LastName="Last"
```

** Install Ops Manager Resource

There is a sample in `mongodb-enterprise-kubernetes` repository that can be used to deploy Ops Manager. However in our demo we will use a slightly modified definition `opsmanager/ops-manager.yaml`. The main difference is few additional configurations:
* Application Database version is removed to allow Operator to manage Version of Backing Database. This is prefered solution especially when our Kubernetes cluster has no access to the Internet
* spec.configuration contains few OpsManager settings:
   mms.preflight.run: "false" - will disable verifications used when OpsManager runs inside a VM.
   mms.ignoreInitialUiSetup: "true" - will disable startup Wizard 
   all other properties are reqires for the minimal initial configuration of OpsManager
* Local Mode configuration
   automation.versions.source: "local"
   automation.versions.directory: "/mongodb-ops-manager/mongodb-releases/" - location of MongoDB packages
* spec.backup is enabled but no other backup configuration is provided in this step.

```bash
$ kubectl apply -f samples/ops-manager/ops-manager.yaml
```
 
This might take 5-7 minute for Operator to provision nessesary Kuberentes resources and for OpsManager to start up and initialise.

To montior installation progress:
* watch for ops-manager-0 pod to get into running stage. Tailing Operator logs would provide more information
* as soon as ops-manager-0 pod is in Running stage, tailing logs would provide information about OpsManager startup progress

In our example we use Kuberentes loadbalancer to expose OpsManager outside of cluster. As soon as Ops Manager is running we could get a url of external service endpoint.

```bash
$ kubectl get svc
```

Expect to get a line similar to this example.
ps-manager-svc-ext   LoadBalancer   10.100.195.127   a754a2e4f42c811eab34416328af91c3-1037012861.us-east-1.elb.amazonaws.com   8080:32209/TCP   15h

Ops Manager is exposes on this url http://a754a2e4f42c811eab34416328af91c3-1037012861.us-east-1.elb.amazonaws.com:8080

Note: TLS configuration will be avaialble in few weeks. Alternativly it is possilbe to use Ingress controller like nginx or Traefik with Letsencrypt to secure this endpoint.

Note: User Name and password for Admin user has been defined above in `adminopsmanager` secret.

** Since we are running Ops Manager in Local Mode we need to copy MongoDB releases into designated folder in Ops Manager. 

First we need to download nessesary MongoDB .tgz file locally from https://www.mongodb.com/download-center/enterprise

** Copy packages needed to launch MongoDB clusters in Local Mode.
Example of Mongodb 4.2.2 Enterpise package
```bash
$ kubectl cp  ~/Downloads/mongodb-linux-x86_64-enterprise-ubuntu1604-4.2.2.tgz ops-manager-0:/mongodb-ops-manager/mongodb-releases/mongodb-linux-x86_64-enterprise-ubuntu1604-4.2.2.tgz
```

Note: Operator v 1.4.2 does not create Persistent Volume for this location. However this will be addressed in 1.4.3.

* Now we are ready to Configure Ops Manager Backup

** Apply Backup S3 bucket keys
```bash
kubectl create secret generic s3-credentials   --from-literal=accessKey="" --from-literal=secretKey=""
```
** Deploy DataBases needed for Backup infrastructure 
```bash
kubectl apply opsmanager/backup-db.yaml
```
** Apply new OpsManager configuration to configure Backup
```bash
kubectl apply -f opsmanager/ops-manager-backup.yaml
```

* At this point we are ready to depoy MongoDB clusters.

We included few sample files to deploy MongoDB clusters

`./mongodb-demo/` contains few of these examples

In order to deploy mongodb cluster we need to create ConfigMap and MongoDB Resource.

Note: We continue to use key generated by Operator when it deployed Ops Manager 'ops-manager-admin-key' in this example.
For a more secure configuration, it is advisable to create a key with restricted permissions.
Open the Ops Manager application. In the UI, generate a new API key by selecting: “UserName -> Account -> Public API Access”
and then create new secret that could be used to create MongoDB clusters
`kubectl create secret generic backup-credentials  --from-literal="user=arjwufgq" --from-literal="publicApiKey=ec7542cf-c1f9-452e-8519-000bca0ae57d"`

Modify demo-cluser-1.yaml and replace baseUrl with OpsManager URL that was deployed in this example. 
If parameter 'data.orgId' is excluded Operator will create brand new OpsManager organization with the same name as `data.project`
```bash
kubectl apply -f mongodb_demo/demo-cluser-1.yaml
```

Now we can deploy MongoDB Cluster

```bash
kubectl apply -f mongodb_demo/demo-mongodb-cluster-1
```

