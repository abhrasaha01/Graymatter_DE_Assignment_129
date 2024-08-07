# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

def square(num):
    return num**2

# COMMAND ----------

def half(num):
    return num/2

# COMMAND ----------

square_udf = udf(square,IntegerType())

# COMMAND ----------

half_udf = udf(half,DoubleType())
