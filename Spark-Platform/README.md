# Spark Connect on Kubernetes with Polaris + MinIO

This project deploys a **Spark Connect server** on Kubernetes integrated
with:

-   **Apache Iceberg**
-   **Polaris REST Catalog**
-   **MinIO / S3-compatible storage**

It includes: - Kubernetes deployment manifest - Deployment helper
script - Sample batch PySpark job - Instructions for interactive Spark
Connect sessions

------------------------------------------------------------------------

## Architecture

PySpark Client 
        ↓ 
Spark Connect Server (Driver) 
        ↓ 
Spark Executors
(Kubernetes Pods) 
    ↓                   ↓ 
Polaris Catalog | MinIO / S3 Object

Spark Connect clients submit **logical plans over gRPC**, executed by
the Spark Connect server.

------------------------------------------------------------------------

## Prerequisites

Ensure the following infrastructure already exists:

-   Kubernetes cluster
-   kubectl configured
-   MinIO / S3-compatible object storage
-   Polaris Iceberg REST catalog
-   Kubernetes namespace `spark-platform`

------------------------------------------------------------------------

## Repository Structure

├── README.md
├── deploy.sh
├── spark-connect-deployment.yaml
└── sample-pyspark-batch-job.py

------------------------------------------------------------------------

## Deploy Spark Connect

Make deployment script executable:

chmod +x deploy.sh

Run deployment:

./deploy.sh

Deployment script:

#!/usr/bin/env bash set -euo pipefail

kubectl apply -f spark-connect-deployment.yaml

echo echo "Resources:" kubectl get all -n spark-platform echo echo
"Ingress:" kubectl get ingress -n spark-platform echo echo "Pods:"
kubectl get pods -n spark-platform -w

------------------------------------------------------------------------

## Verify Deployment

kubectl get all -n spark-platform kubectl logs -n spark-platform
deploy/spark-connect -f

Expected:

-   Spark Connect server pod running
-   Executors start when jobs execute

------------------------------------------------------------------------

## Sample Batch Job

sample-pyspark-batch-job.py

from pyspark.sql import SparkSession

spark = ( SparkSession.builder
.remote("sc://spark-connect.spark-platform.svc.cluster.local:15002")
.getOrCreate() )

print("=== SHOW CATALOGS ===") spark.sql("SHOW
CATALOGS").show(truncate=False)

print("=== SHOW NAMESPACES IN polaris ===") spark.sql("SHOW NAMESPACES
IN polaris").show(truncate=False)

spark.sql("CREATE NAMESPACE IF NOT EXISTS polaris.demo")

spark.sql(""" CREATE TABLE IF NOT EXISTS polaris.demo.people_batch ( id
BIGINT, name STRING ) USING iceberg """)

spark.sql(""" INSERT INTO polaris.demo.people_batch VALUES (11,
'Samuel'), (12, 'Rafael'), (13, 'Saraguel') """)

spark.sql("SELECT \* FROM polaris.demo.people_batch ORDER BY id").show()

spark.stop()

------------------------------------------------------------------------

## Interactive Spark Connect Session

Start temporary Spark client pod:

kubectl run -it --rm spark-client -n spark-platform
--image=apache/spark:4.0.2-scala2.13-java17-python3-ubuntu
--restart=Never -- /bin/bash

Install required Python libraries:

export HOME=/tmp export PYTHONUSERBASE=/tmp/.pyuser

python3 -m pip install --user pyspark==4.0.2 grpcio grpcio-status pandas
pyarrow

Verify installation:

python3 -c "import pyspark; print(pyspark.\_\_version\_\_)"

Start Python:

python3

Connect to Spark:

from pyspark.sql import SparkSession

spark = ( SparkSession.builder
.remote("sc://spark-connect.spark-platform.svc.cluster.local:15002")
.getOrCreate() )

spark.range(10).show()

spark.sql("SHOW CATALOGS").show(truncate=False) spark.sql("SHOW
NAMESPACES IN polaris").show(truncate=False)

spark.sql("CREATE NAMESPACE IF NOT EXISTS polaris.demo")

spark.sql(""" CREATE TABLE IF NOT EXISTS polaris.demo.people ( id
BIGINT, name STRING ) USING iceberg """)

spark.sql("INSERT INTO polaris.demo.people VALUES (1, 'john'), (2,
'peter')") spark.sql("SELECT \* FROM polaris.demo.people").show()

------------------------------------------------------------------------

## Connection Strings

Inside cluster:

sc://spark-connect.spark-platform.svc.cluster.local:15002

External:

sc://sparkconnect.homelab.com:443

------------------------------------------------------------------------

## Required Python Packages

pyspark==4.0.2\
grpcio\
grpcio-status\
pandas\
pyarrow

Install:

python3 -m pip install pyspark==4.0.2 grpcio grpcio-status pandas
pyarrow

------------------------------------------------------------------------

## Spark UI

Access Spark Web UI via:

kubectl port-forward -n spark-platform deploy/spark-connect 4040:4040

Open browser:

http://localhost:4040

------------------------------------------------------------------------

## Troubleshooting

Check Spark logs:

kubectl logs -n spark-platform deploy/spark-connect -f

Check services:

kubectl get svc -n spark-platform

Check ingress:

kubectl get ingress -n spark-platform

------------------------------------------------------------------------

## Next Steps

-   Build custom Spark image
-   Expose Spark Connect via gRPC ingress
-   Add CI/CD pipeline for Spark jobs
-   Integrate with Jupyter / VS Code
