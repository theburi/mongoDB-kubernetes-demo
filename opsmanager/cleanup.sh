
kubectl delete -f opsmanager/ops-manager-oplog.yaml
kubectl delete -f opsmanager/ops-manager-meta.yaml
kubectl delete -f opsmanager/ops-manager-backup.yaml
kubectl delete -f opsmanager/backup-db.yaml
kubectl delete pvc data-demo-mongodb-oplog-0 data-demo-mongodb-oplog-1 data-demo-mongodb-oplog-2
kubectl delete pvc data-my-mongodb-s3-0 data-my-mongodb-s3-1 data-my-mongodb-s3-2
kubectl delete pvc data-ops-manager-db-0 data-ops-manager-db-1 data-ops-manager-db-2
kubectl delete pvc head-ops-manager-backup-daemon-0
kubectl delete -f mongodb_demo/demo-mongodb-cluster-1.yaml

