from pyspark.sql import SparkSession

#sc://spark-connect.spark-platform.svc.cluster.local:15002
# OR
# sc://sparkconnect.homelab.com:443
spark = (
    SparkSession.builder
    .remote("sc://spark-connect.spark-platform.svc.cluster.local:15002")
    .getOrCreate()
)

print("=== SHOW CATALOGS ===")
spark.sql("SHOW CATALOGS").show(truncate=False)

print("=== SHOW NAMESPACES IN polaris ===")
spark.sql("SHOW NAMESPACES IN polaris").show(truncate=False)

spark.sql("CREATE NAMESPACE IF NOT EXISTS polaris.demo")

spark.sql("""
CREATE TABLE IF NOT EXISTS polaris.demo.people_batch (
    id BIGINT,
    name STRING
) USING iceberg
""")

spark.sql("""
INSERT INTO polaris.demo.people_batch VALUES
    (11, 'Samuel'),
    (12, 'Rafael'),
    (13, 'Saraguel')
""")

print("=== FINAL DATA ===")
spark.sql("SELECT * FROM polaris.demo.people_batch ORDER BY id").show()

spark.stop()