# Databricks notebook source
from pyspark.storagelevel import StorageLevel

# COMMAND ----------

jdbc_url = "jdbc:sqlserver://gmde-server-1716.database.windows.net:1433;database=GMDE_DB_1716"
jdbc_properties = {
    "user":"sql1716",
    "password":"",    #erased it after running the cell
    "driver":"com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# COMMAND ----------

# MAGIC %md
# MAGIC ###Connecting SQL Database to Databricks

# COMMAND ----------

table_name = "saleslt.customer"
df_Customer = spark.read.jdbc(url = jdbc_url, table = table_name, properties = jdbc_properties)
df_Customer.display()

# COMMAND ----------

#Get the size of file
spark.conf.get("spark.sql.files.maxPartitionBytes")

# COMMAND ----------

df_Customer.rdd.getNumPartitions()

# COMMAND ----------

# MAGIC %md
# MAGIC ####Increasing and decreasing number of partitions

# COMMAND ----------

df_Customer = df_Customer.repartition(20)

# COMMAND ----------

df_Customer = df_Customer.coalesce(2)

# COMMAND ----------

# MAGIC %md
# MAGIC ####Creating cache

# COMMAND ----------

#Import storageLevel function from pyspark.storage level(Imported above)
df_Customer.persist(StorageLevel.MEMORY_ONLY)
