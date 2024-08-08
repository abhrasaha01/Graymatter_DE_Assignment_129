# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

# MAGIC %md
# MAGIC ####Connecting SQL Database

# COMMAND ----------

jdbc_url = "jdbc:sqlserver://gmde-server-1716.database.windows.net:1433;database=GMDE_DB_1716"
jdbc_properties = {
    "user":"sql1716",
    "password":"",    #erased it after running the cell
    "driver":"com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# COMMAND ----------

# MAGIC %md
# MAGIC ##Create customer and sales table df

# COMMAND ----------

customer_table = "saleslt.customer"
sales_header_table = "saleslt.salesorderheader"
sales_detail_table = "saleslt.salesorderdetail"
df_Customer = spark.read.jdbc(url = jdbc_url, table = customer_table, properties = jdbc_properties)
df_SalesOrderHeader = spark.read.jdbc(url = jdbc_url, table = sales_header_table, properties = jdbc_properties)
df_SalesOrderDetail = spark.read.jdbc(url = jdbc_url, table = sales_detail_table, properties = jdbc_properties)

# COMMAND ----------

df_SalesOrderHeader.display()

# COMMAND ----------

df_sales_new = df_SalesOrderHeader.join(df_SalesOrderDetail, df_SalesOrderHeader.SalesOrderID == df_SalesOrderDetail.SalesOrderID).select(df_SalesOrderHeader["SalesOrderID"],df_SalesOrderHeader["OrderDate"].cast(DateType()),df_SalesOrderHeader["SalesOrderNumber"],df_SalesOrderHeader["CustomerID"],df_SalesOrderDetail["SalesOrderDetailID"],df_SalesOrderDetail["OrderQty"],df_SalesOrderDetail["ProductID"],df_SalesOrderDetail["UnitPrice"])

# COMMAND ----------

df_sales_new.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ####Filtering data between certain range

# COMMAND ----------

start_date = dbutils.widgets.get("Start_date")
end_date = dbutils.widgets.get("End_date")

# COMMAND ----------

df_sales_new = df_sales_new.filter((df_sales.OrderDate >= start_date) & (df_sales.OrderDate <= end_date))

# COMMAND ----------

df_sales_new.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ####Replacing NaN values with 0

# COMMAND ----------

df_sales_new = df_sales_new.na.fill(0)

# COMMAND ----------

# MAGIC %md
# MAGIC ####Creting TotalSales column

# COMMAND ----------

df_sales_new = df_sales_new.withColumn("TotalSales",col('OrderQty')*col('UnitPrice'))

# COMMAND ----------

# MAGIC %md
# MAGIC ####Aggregating no.of orders, total sales per customer

# COMMAND ----------

df_gb_Customer = df_sales_new.groupBy("CustomerID").agg(count("SalesOrderID"),sum('TotalSales'))

# COMMAND ----------

df_gb_Customer.display()

# COMMAND ----------

df_gb_Customer = df_gb_Customer.withColumnRenamed("SalesCount","OrderCount")
df_gb_Customer = df_gb_Customer.withColumnRenamed("sum(TotalSales)","TotalSales")

# COMMAND ----------

# MAGIC %md
# MAGIC ####Joining the aggregate table with customer table

# COMMAND ----------

df_Pre_Final = df_Customer.join(df_gb_Customer, on = "CustomerID").select(df_Customer["CustomerID"],df_Customer["FirstName"],df_Customer["MiddleName"],df_Customer["LastName"],df_gb_Customer["OrderCount"],df_gb_Customer["TotalSales"])

# COMMAND ----------

df_Pre_Final.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ####Saving dataframe as delta table

# COMMAND ----------

df_Pre_Final.write.format("delta").save("/mnt/input/Result")

# COMMAND ----------

# MAGIC %sql
# MAGIC create table result_table
# MAGIC using delta
# MAGIC options(path "abfss://input@adlsgmde1716.dfs.core.windows.net/Result")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from result_table

# COMMAND ----------

# MAGIC %md
# MAGIC ####Optimizing table using cluster by clause

# COMMAND ----------

# MAGIC %sql
# MAGIC select * into new_result_table
# MAGIC from result_table

# COMMAND ----------

# MAGIC %sql
# MAGIC optimize new_result_table
# MAGIC cluster by CustomerID

# COMMAND ----------

# MAGIC %md
# MAGIC ###Optimizing data using ZORDER

# COMMAND ----------

# MAGIC %sql
# MAGIC optimize result_table
# MAGIC zorder by CustomerID
