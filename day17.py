# Databricks notebook source
from pyspark.sql.types import IntegerType, StringType, StructType, StructField

# COMMAND ----------

# MAGIC %md
# MAGIC ####Create a schema structure

# COMMAND ----------

schema = StructType([
    StructField("ID",IntegerType(),True),
    StructField("Name",StringType(),True),
    StructField("Age",IntegerType(),True)
]
)

# COMMAND ----------

# MAGIC %md
# MAGIC ####Reading Sample File

# COMMAND ----------

df_source = spark.read.option("Header",True).schema(schema).csv("/FileStore/sample.csv")
df_source.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ####Creating a mount to access ADF Container

# COMMAND ----------

dbutils.fs.mount(
    source = "wasbs://input@adlsgmde1716.blob.core.windows.net",
    mount_point ="/mnt/input",
    extra_configs = {"fs.azure.account.key.adlsgmde1716.blob.core.windows.net":dbutils.secrets.get(scope = "ADLSkeyScope", key = "KeyADLS")})

# COMMAND ----------

dbutils.fs.ls("/mnt/input")

# COMMAND ----------

# MAGIC %md
# MAGIC ####Reading a file from ADF using Mount

# COMMAND ----------

df_mounted = spark.read.option("Header", True).option("inferschema",True).csv("/mnt/input/sales_asisa_24_07_2024.csv")
df_mounted.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ####Writing the mounted DataFrame into different formats

# COMMAND ----------

df_mounted.write.csv("mnt/input/ADBoutput")

# COMMAND ----------

df_mounted.write.parquet("mnt/input/parquet")

# COMMAND ----------

df_mounted.write.format("Delta").saveAsTable("sales_asia")

# COMMAND ----------

df_mounted.write.format("delta").save("/mnt/input/sales_asia")

# COMMAND ----------

# MAGIC %md
# MAGIC ####Creating table at external location

# COMMAND ----------

# MAGIC %sql
# MAGIC create table ext_sales_asia
# MAGIC using delta
# MAGIC options (path 'abfss://input@adlsgmde1716.dfs.core.windows.net/sales_asia')

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from ext_sales_asia

# COMMAND ----------

# MAGIC %sql
# MAGIC delete from ext_sales_asia where SaleID = 17

# COMMAND ----------

# MAGIC %sql
# MAGIC update ext_sales_asia set Quantity = 5 where SaleID = 16

# COMMAND ----------

# MAGIC %md
# MAGIC ####Describing table using various describe methods

# COMMAND ----------

# MAGIC %sql
# MAGIC describe ext_sales_asia

# COMMAND ----------

# MAGIC %sql
# MAGIC describe history ext_sales_asia

# COMMAND ----------

# MAGIC %sql
# MAGIC describe detail ext_sales_asia

# COMMAND ----------

# MAGIC %sql
# MAGIC describe extended ext_sales_asia

# COMMAND ----------

# MAGIC %sql
# MAGIC insert into ext_sales_asia values(28, 223, 1401,5, getdate(), 140.65)

# COMMAND ----------

# MAGIC %md
# MAGIC ####Optimizing table using ZORDER

# COMMAND ----------

# MAGIC %sql
# MAGIC optimize ext_sales_asia
# MAGIC zorder by (SaleID,SalesRepID)

# COMMAND ----------


