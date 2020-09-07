** Configuraing Vertical Pod Autoscaler

1. Ensure VPA is installed
    `kubectl -n kube-system get deployment/metrics-server`
    if this command retern no resource you don't have VPA running

2. Install Metric Server
    ```bash
    DOWNLOAD_URL=$(curl -Ls "https://api.github.com/repos/kubernetes-sigs/metrics-server/releases/latest" | jq -r .tarball_url)
    DOWNLOAD_VERSION=$(grep -o '[^/v]*$' <<< $DOWNLOAD_URL)
    curl -Ls $DOWNLOAD_URL -o metrics-server-$DOWNLOAD_VERSION.tar.gz
    mkdir metrics-server-$DOWNLOAD_VERSION
    tar -xzf metrics-server-$DOWNLOAD_VERSION.tar.gz --directory metrics-server-$DOWNLOAD_VERSION --strip-components 1
    kubectl apply -f metrics-server-$DOWNLOAD_VERSION/deploy/1.7/

    ```
    Verify it again
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
metrics-server   1/1     1            1           12s


3. Install Vertical Auto Scaler

Clone the kubernetes/autoscaler GitHub repository.

`git clone https://github.com/kubernetes/autoscaler.git`

Change to the vertical-pod-autoscaler directory.

`cd autoscaler/vertical-pod-autoscaler/`

(Optional) If you have already deployed another version of the Vertical Pod Autoscaler, remove it with the following command.
`./hack/vpa-down.sh`

Deploy the Vertical Pod Autoscaler to your cluster with the following command.
`./hack/vpa-up.sh`
Verify that the Vertical Pod Autoscaler pods have been created successfully.

`kubectl get pods -n kube-system`