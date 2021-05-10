# Databricks notebook source
# MAGIC %md
# MAGIC ## Connecting to blob
# MAGIC Connecting using built-in library dbutils and authentecating with a SAS token. 
# MAGIC 
# MAGIC **This is a simple example:** Secrets should be saved as databricks secrets, and we can optionally authenticate with a storage account key. For more info see [Azure docs](https://docs.microsoft.com/en-us/azure/databricks/data/data-sources/azure/azure-storage). The mount is a one-time command where token must be inserted manually.

# COMMAND ----------

dbutils.fs.mount(
  source="wasbs://maindata@kobricksaccount.blob.core.windows.net",  # WASB url of blob
  mount_point="/mnt/maindata",  # where to mount blob here in databricks
  extra_configs = {  # authentication
    "fs.azure.sas.maindata.kobricksaccount.blob.core.windows.net": "<my-sas-key>"
  }
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exploring the data
# MAGIC Common file utilities are availablie through `dbutils.fs` as documented by [Databricks](https://docs.databricks.com/dev-tools/databricks-utils.html). For reading data we can use the [`DataFrameReader`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql.html) returned by [`spark.read`](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.SparkSession.read.html#pyspark.sql.SparkSession.read). Here we use the [csv reader](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.DataFrameReader.csv.html#pyspark.sql.DataFrameReader.csv) for importing our csv file.
# MAGIC 
# MAGIC **Note:** 
# MAGIC - The `spark` object is an instance of [`pyspark.sql.SparkSession`](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.SparkSession.html#pyspark.sql.SparkSession). Which is automaticlly created and imported to databricks notebooks. 
# MAGIC - Remember pressing `tab` or `shift+tab` for help on object properties.

# COMMAND ----------

dbutils.fs.ls('/mnt/maindata/test')

# COMMAND ----------

df = spark.read.csv('/mnt/maindata/test/no2_consumption_temperature_2020.csv', header=True)
df.show(5)
print('Format-->', df.dtypes)

# COMMAND ----------

# MAGIC %md
# MAGIC Notice datatype for each column is inferred as string. To fix this we specify datatype in `schema` parameter. For more robust use one should consider making the schema as a [`StructType`](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.types.StructType.html#pyspark.sql.types.StructType).

# COMMAND ----------

# struct = Struct
struct_df = spark.read.csv(
  '/mnt/maindata/test/no2_consumption_temperature_2020.csv', 
  header=True,
  schema='Date TIMESTAMP, consumption DOUBLE, temperature DOUBLE',
)
struct_df.show(5)
print('Format -->', struct_df.dtypes)

# COMMAND ----------

# MAGIC %md
# MAGIC Additionally we can convert the Spark dataframe to a Pandas dataframe. However, this removes performance benefits of spark and should be avoided on large datasets.

# COMMAND ----------

pdf = struct_df.toPandas()
pdf = pdf.set_index('Date')
pdf

# COMMAND ----------

pdf.plot(subplots=True, figsize=(14,6))
