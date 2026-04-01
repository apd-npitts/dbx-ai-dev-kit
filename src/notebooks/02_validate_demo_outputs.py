# Databricks notebook source
dbutils.widgets.text("catalog", "main")
dbutils.widgets.text("schema", "genie_codex_demo")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

checks = {
    "gold_site_operations_hourly": f"`{catalog}`.`{schema}`.`gold_site_operations_hourly`",
    "gold_device_daily_summary": f"`{catalog}`.`{schema}`.`gold_device_daily_summary`",
}

results = []
for name, table_name in checks.items():
    row_count = spark.sql(f"SELECT COUNT(*) AS row_count FROM {table_name}").collect()[0]["row_count"]
    results.append((name, row_count))
    print(f"{name}: {row_count} rows")

display(spark.createDataFrame(results, ["table_name", "row_count"]))

display(
    spark.sql(
        f"""
        SELECT *
        FROM `{catalog}`.`{schema}`.`gold_site_operations_hourly`
        ORDER BY critical_events DESC, event_count DESC
        LIMIT 20
        """
    )
)
