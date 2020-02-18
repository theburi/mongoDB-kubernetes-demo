
helm upgrade prometheus-chart stable/prometheus-operator --set grafana.sidecar.dashboards.enabled=true -f prom-values.yaml 


helm upgrade --install mdb-prom-exporter stable/prometheus-mongodb-exporter -f "{'mongodb.url': 'mongo+srv://demo-mongodb-cluster-1-svc.mongodb.svc.cluster.local:27017'}"


wget https://raw.githubusercontent.com/percona/grafana-dashboards/master/dashboards/MongoDB_Overview.json
kubectl create cm grafana-mongodb-overview --from-file=MongoDB_Overview.json

kubectl label cm grafana-mongodb-overview grafana_dashboard=mongodb-overview

** Grafana

Default credentials
User: Admin Password: prom-operator