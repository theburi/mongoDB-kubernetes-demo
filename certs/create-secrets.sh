# First Member Certificate
kubectl -n mongodb get secret/ops-manager-db-0 -o jsonpath='{.data.tls\.crt}' | base64 --decode > ops-manager-db-0-pem
kubectl -n mongodb get secret/ops-manager-db-0 -o jsonpath='{.data.tls\.key}' | base64 --decode >> ops-manager-db-0-pem

# Second Member Certificate
kubectl -n mongodb get secret/ops-manager-db-1 -o jsonpath='{.data.tls\.crt}' | base64 --decode > ops-manager-db-1-pem
kubectl -n mongodb get secret/ops-manager-db-1 -o jsonpath='{.data.tls\.key}' | base64 --decode >> ops-manager-db-1-pem

# Third Member Certificate
kubectl -n mongodb get secret/ops-manager-db-2 -o jsonpath='{.data.tls\.crt}' | base64 --decode > ops-manager-db-2-pem
kubectl -n mongodb get secret/ops-manager-db-2 -o jsonpath='{.data.tls\.key}' | base64 --decode >> ops-manager-db-2-pem

rm ops-manager-db-*

kubectl -n mongodb create secret generic ops-manager-db-cert --from-file=ops-manager-db-0-pem --from-file=ops-manager-db-1-pem --from-file=ops-manager-db-2-pem



cat ca.crt > ca-pem
kubectl -n mongodb create configmap ca-appdb --from-file=ca-pem


kubectl -n mongodb get secret/ops-manager -o jsonpath='{.data.tls\.crt}' | base64 --decode > server.pem
kubectl -n mongodb get secret/ops-manager -o jsonpath='{.data.tls\.key}' | base64 --decode >> server.pem

kubectl -n mongodb delete secret ops-manager-app-cert
kubectl -n mongodb create secret generic ops-manager-app-cert --from-file=server.pem
rm server.pem

{"apiVersion":"v1", "items":[]interface {}{map[string]interface {}
{"apiVersion":"mongodb.com/v1", "kind":"MongoDBOpsManager", 
"metadata":map[string]interface {}
    {"annotations":map[string]interface {}
        {"kubectl.kubernetes.io/last-applied-configuration":"{\"apiVersion\":\"mongodb.com/v1\",\"kind\":\"MongoDBOpsManager\",\"metadata\":{\"annotations\":{},\"name\":\"ops-manager\",\"namespace\":\"mongodb\"},\"spec\":{\"adminCredentials\":\"adminopsmanager\",\"applicationDatabase\":{\"members\":3,\"persistent\":true,\"podSpec\":{\"cpu\":\"0.25\",\"memory\":\"300Mi\",\"memoryRequests\":\"250Mi\"},\"security\":{\"tls\":{\"ca\":\"ca-appdb\",\"secretRef\":{\"name\":\"ops-manager-db-cert\"}}}},\"backup\":{\"enabled\":false},\"configuration\":{\"mms.adminEmailAddr\":\"test@test.com\",\"mms.fromEmailAddr\":\"test@test.com\",\"mms.ignoreInitialUiSetup\":\"true\",\"mms.mail.hostname\":\"mail.example.com\",\"mms.mail.port\":\"465\",\"mms.mail.transport\":\"smtps\",\"mms.replyToEmailAddr\":\"test@test.com\"},\"externalConnectivity\":{\"type\":\"LoadBalancer\"},\"replicas\":1,\"security\":{\"tls\":{\"secretRef\":{\"name\":\"ops-manager-app-cert\"}}},\"statefulSet\":{\"spec\":{\"template\":{\"spec\":{\"containers\":[{\"name\":\"mongodb-ops-manager\",\"resources\":{\"limits\":{\"memory\":\"3G\"},\"requests\":{\"memory\":\"2G\"}}}]}}}},\"version\":\"4.4.0\"}}\n"}, "creationTimestamp":"2020-08-06T18:18:44Z", "generation":2, "name":"ops-manager", "namespace":"mongodb", "resourceVersion":"226864", "selfLink":"/apis/mongodb.com/v1/namespaces/mongodb/opsmanagers/ops-manager", "uid":"358b9c5f-e99d-4038-9443-7b776a18b02e"},
        "spec":map[string]interface {}
            {"adminCredentials":"adminopsmanager", "applicationDatabase":map[string]interface {}{"members":3, "persistent":true, 
                "podSpec":map[string]interface {}{"cpu":"0.25", "memory":"300Mi", "memoryRequests":"250Mi"}, "security":map[string]interface {}{"tls":map[string]interface {}{"ca":"ca-appdb", "secretRef":map[string]interface {}{"name":"ops-manager-db-cert"}}}}, "backup":map[string]interface {}{"enabled":false}, "configuration":map[string]interface {}{"mms.adminEmailAddr":"test@test.com", "mms.fromEmailAddr":"test@test.com", "mms.ignoreInitialUiSetup":"true", "mms.mail.hostname":"mail.example.com", "mms.mail.port":"465", "mms.mail.transport":"smtps", "mms.replyToEmailAddr":"test@test.com"}, "externalConnectivity":map[string]interface {}{"type":"LoadBalancer"}, "replicas":1, "security":map[string]interface {}{"tls":map[string]interface {}{"secretRef":map[string]interface {}{"name":"ops-manager-app-cert"}}}, "statefulSet":map[string]interface {}{"spec":map[string]interface {}{"template":map[string]interface {}{"spec":map[string]interface {}{"containers":[]interface {}{map[string]interface {}{"name":"mongodb-ops-manager", "resources":map[string]interface {}{"limits":map[string]interface {}{"memory":"3G"}, "requests":map[string]interface {}{"memory":"2G"}}}}}}}}, "version":"4.4.0"}, "status":map[string]interface {}{"applicationDatabase":map[string]interface {}{"lastTransition":"2020-08-07T09:04:34Z", "members":3, "phase":"Running", "type":"ReplicaSet", "version":"4.2.2-ent"}, "backup":map[string]interface {}{"phase":""}, "opsManager":map[string]interface {}{"lastTransition":"2020-08-07T09:04:36Z", "phase":"Running", "replicas":1, "url":"https://ops-manager-svc.mongodb.svc.cluster.local:8443", "version":"4.4.0"}}}}, "kind":"List", "metadata":map[string]interface {}{"resourceVersion":"", "selfLink":""}}
