# Databricks notebook source
jdbc_url = "jdbc:sqlserver://gmde-server-1716.database.windows.net:1433;database=GMDE_DB_1716"
jdbc_properties = {
    "user":"sql1716",
    "password":"",    #erased it after running the cell
    "driver":"com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from result_table

# COMMAND ----------

# MAGIC %md
# MAGIC ####DEEP CLONING

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE deepCloneTale CLONE sales_asia

# COMMAND ----------



# COMMAND ----------

# MAGIC %sql
# MAGIC select * from deepCloneTale

# COMMAND ----------

# MAGIC %md
# MAGIC ####SHALLOW CLONING

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE shallowClone SHALLOW CLONE sales_asia

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from shallowClone

# COMMAND ----------

# MAGIC %sql
# MAGIC insert into deepCloneTale values(21,121,1021,4,getdate(),79.96)

# COMMAND ----------

# MAGIC %sql
# MAGIC update deepCloneTale set SaleAmount = 44 where SaleID = 17

# COMMAND ----------

# MAGIC %sql
# MAGIC insert into shallowClone values(22,122,1022,4,getdate(),79.96)

# COMMAND ----------

# MAGIC %sql
# MAGIC update shallowClone set SaleID = 23 where SaleID = 21

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from sales_asia

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from deepClonetale

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from shallowClone

# COMMAND ----------

# MAGIC %sql
# MAGIC insert into sales_asia values(25,125,1025,5,getdate(),79.96)

# COMMAND ----------

# MAGIC %sql
# MAGIC describe history shallowClone
