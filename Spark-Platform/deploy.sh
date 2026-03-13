#!/usr/bin/env bash
set -euo pipefail

kubectl apply -f spark-connect-deployment.yaml

echo
echo "Resources:"
kubectl get all -n spark-platform
echo
echo "Ingress:"
kubectl get ingress -n spark-platform
echo
echo "Pods:"
kubectl get pods -n spark-platform -w

#chmod +x deploy.sh
#./deploy.sh