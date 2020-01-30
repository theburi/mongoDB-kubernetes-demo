Deploy Ops Manager in Kuberentes with MongoDB Enterprise Operator
** Cleanup Demo environment

bash opsmanager/cleanup.sh

** Apply secrets for Ops manager
kubectl create secret generic "adminopsmanager" --from-literal=Username="test@test.com" --from-literal=Password='KubeTest12!' --from-literal=FirstName="First" --from-literal=LastName="Last"


** Launch Ops Manager without Backup

kubectl apply -f opsmanager/ops-manager.yaml 

** Copy file needed to launch clusters in Local Mode

kubectl cp  ~/Downloads/mongodb-linux-x86_64-enterprise-ubuntu1604-4.2.2.tgz ops-manager-0:/mongodb-ops-manager/mongodb-releases/mongodb-linux-x86_64-enterprise-ubuntu1604-4.2.2.tgz

** Apply Backup S3 bucket keys

kubectl create secret generic s3-credentials   --from-literal=accessKey="AKIAWZC4C4LCBIFWEKW7" --from-literal=secretKey="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"

** Apply DataBases needed for Backup

kubectl apply opsmanager/backup-db.yaml

** Apply new OpsManager configuration to configure Backup

kubectl apply -f opsmanager/ops-manager-backup.yaml