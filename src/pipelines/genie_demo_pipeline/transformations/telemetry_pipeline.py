from pyspark import pipelines as dp
from pyspark.sql import functions as F


raw_volume_path = spark.conf.get("raw_volume_path")
schema_location_base = spark.conf.get("schema_location_base")


@dp.table(name="bronze_telemetry_events")
def bronze_telemetry_events():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.inferColumnTypes", "true")
        .option(
            "cloudFiles.schemaLocation",
            f"{schema_location_base}/bronze_telemetry_events",
        )
        .load(raw_volume_path)
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_file", F.col("_metadata.file_path"))
    )


@dp.table(name="silver_device_health")
def silver_device_health():
    return (
        spark.readStream.table("bronze_telemetry_events")
        .withColumn(
            "severity",
            F.when(F.col("temperature_c") >= 90, F.lit("critical"))
            .when(F.col("temperature_c") >= 80, F.lit("warning"))
            .otherwise(F.lit("normal")),
        )
        .withColumn(
            "battery_state",
            F.when(F.col("battery_pct") < 15, F.lit("replace"))
            .when(F.col("battery_pct") < 35, F.lit("watch"))
            .otherwise(F.lit("healthy")),
        )
        .withColumn("event_date", F.to_date("event_ts"))
        .withColumn("event_hour", F.date_trunc("hour", "event_ts"))
    )


@dp.materialized_view(name="gold_site_operations_hourly")
def gold_site_operations_hourly():
    return (
        spark.read.table("silver_device_health")
        .groupBy("site_id", "region", "event_hour")
        .agg(
            F.count("*").alias("event_count"),
            F.sum(F.when(F.col("severity") == "critical", 1).otherwise(0)).alias(
                "critical_events"
            ),
            F.round(F.avg("temperature_c"), 2).alias("avg_temperature_c"),
            F.round(F.avg("battery_pct"), 2).alias("avg_battery_pct"),
        )
    )


@dp.materialized_view(name="gold_device_daily_summary")
def gold_device_daily_summary():
    return (
        spark.read.table("silver_device_health")
        .groupBy("event_date", "device_type")
        .agg(
            F.countDistinct("device_id").alias("active_devices"),
            F.sum(F.when(F.col("battery_state") == "replace", 1).otherwise(0)).alias(
                "replace_battery_events"
            ),
            F.sum(F.when(F.col("severity") == "critical", 1).otherwise(0)).alias(
                "critical_events"
            ),
            F.round(F.avg("temperature_c"), 2).alias("avg_temperature_c"),
        )
    )
