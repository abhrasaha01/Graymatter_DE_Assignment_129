# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

df_mounted = spark.read.option("Header", True).option("inferschema",True).csv("/mnt/input/sales_asisa_24_07_2024.csv")
df_mounted.display()

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
# MAGIC insert into ext_sales_asia values(31, 253, 1420,5, getdate(), 160.15);
# MAGIC insert into ext_sales_asia values(41, 254, 1440,8, getdate(), 300.24);
# MAGIC insert into ext_sales_asia values(45, 255, 1450,6, getdate(), 260.65);

# COMMAND ----------

ProductID_var = dbutils.widgets.get("ProductID")
print(ProductID_var)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from ext_sales_asia where SalesRepID in ($SalesRepID)

# COMMAND ----------

SalesRepID_var = dbutils.widgets.get("SalesRepID")
#for i in SalesRepID_var:
print(i)

# COMMAND ----------

df_mounted.display()

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from ext_sales_asia

# COMMAND ----------

def double(num):
    return num*2

# COMMAND ----------

# MAGIC %md
# MAGIC ####Registering functions for pyspark and sql

# COMMAND ----------

double_pyspark = udf(double,IntegerType())              #Python
spark.udf.register("double_sql",double,IntegerType())   #SQL

# COMMAND ----------

# MAGIC %md
# MAGIC ####Using the functions in python df and sql table

# COMMAND ----------

df_doubleQty = df_mounted.withColumn("DoubleQty",double_pyspark(col("Quantity")))
df_doubleQty.display()

# COMMAND ----------

# MAGIC %sql
# MAGIC select SaleID, double_sql(Quantity) as DoubleQuantity from ext_sales_asia

# COMMAND ----------

# MAGIC %md
# MAGIC ####Entering a record using parameters

# COMMAND ----------

# MAGIC %sql
# MAGIC insert into ext_sales_asia values($SaleID, $SalesRepID, $ProductID, $Quantity, Getdate(), $SaleAmount)

# COMMAND ----------

# MAGIC %run /Workspace/Users/abhrasaha17@gmail.com/Graymatter_project/Utilities/Basic_Functions

# COMMAND ----------

df_halfQty = df_mounted.withColumn("HalfQty",half_udf(col("Quantity")))
df_halfQty.display()

# COMMAND ----------

df_squareQty = df_mounted.withColumn("SquareQty",square_udf(col("Quantity")))
df_squareQty.display()
