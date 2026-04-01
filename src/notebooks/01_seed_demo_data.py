# Databricks notebook source
dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("schema", "genie_codex_demo")
dbutils.widgets.text("volume_name", "demo_assets")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
volume_name = dbutils.widgets.get("volume_name")

spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{catalog}`.`{schema}`")
spark.sql(f"CREATE VOLUME IF NOT EXISTS `{catalog}`.`{schema}`.`{volume_name}`")

raw_path = f"/Volumes/{catalog}/{schema}/{volume_name}/raw/telemetry_events"

from pyspark.sql import functions as F

events = (
    spark.range(0, 2500)
    .withColumn("device_id", F.concat(F.lit("device-"), F.lpad(F.col("id"), 4, "0")))
    .withColumn(
        "device_type",
        F.element_at(
            F.array(F.lit("compressor"), F.lit("freezer"), F.lit("pump"), F.lit("meter")),
            (F.col("id") % 4) + 1,
        ),
    )
    .withColumn(
        "region",
        F.element_at(
            F.array(F.lit("central"), F.lit("east"), F.lit("south"), F.lit("west")),
            (F.col("id") % 4) + 1,
        ),
    )
    .withColumn("site_id", F.concat(F.lit("site-"), F.lpad((F.col("id") % 18) + 1, 3, "0")))
    .withColumn(
        "event_ts",
        F.from_unixtime(
            F.unix_timestamp(F.current_timestamp()) - ((F.col("id") % 48) * 3600)
        ).cast("timestamp"),
    )
    .withColumn("temperature_c", F.round(55 + (F.rand(7) * 45), 2))
    .withColumn("battery_pct", F.round(5 + (F.rand(11) * 95), 2))
    .withColumn("pressure_kpa", F.round(90 + (F.rand(19) * 55), 2))
    .withColumn("status_code", F.when((F.col("id") % 13) == 0, F.lit("ALERT")).otherwise(F.lit("OK")))
    .drop("id")
)

events.coalesce(1).write.mode("overwrite").json(raw_path)

display(events.limit(20))
print(f"Seeded demo telemetry data into {raw_path}")
