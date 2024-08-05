# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

df01 = spark.read.csv("/FileStore/gmde/googleplaystore.csv")

# COMMAND ----------

df01.display()

# COMMAND ----------

df01.printSchema()

# COMMAND ----------

df02 = spark.read.option("header",True).csv("/FileStore/gmde/googleplaystore.csv")

# COMMAND ----------

df02.display()

# COMMAND ----------

df03 = spark.read.option("header",True).option("inferschema",True).csv("/FileStore/gmde/googleplaystore.csv")

# COMMAND ----------

df03.display()

# COMMAND ----------

df03.printSchema()

# COMMAND ----------

schemas = StructType().add("App",StringType(),True)\
        .add("Category",StringType(),True)\
        .add("Rating",DoubleType(),True)\
        .add("Reviews",IntegerType(),True)\
        .add("Size",StringType(),True)\
        .add("Installs",StringType(),True)\
        .add("Type",StringType(),True)\
        .add("Price",StringType(),True)\
        .add("Content Rating",StringType(),True)\
        .add("Genres",StringType(),True)\
        .add("LastUpdated",StringType(),True)\
        .add("Current Ver",StringType(),True)\
        .add("Android Ver",StringType(),True)

# COMMAND ----------

df04 = spark.read.option("header",True).schema(schemas).csv("/FileStore/gmde/googleplaystore.csv")

# COMMAND ----------

df04.display()

# COMMAND ----------

df04 = df04.withColumn("ReviewRating", col("Rating")*col("Reviews"))

# COMMAND ----------

df04 = df04.withColumn("AC",concat(col("App"),col("Category")))

# COMMAND ----------

df04 = df04.withColumn("Owner",lit("Abhra"))

# COMMAND ----------

df04 = df04.withColumn("new",col("App"))

# COMMAND ----------

df04.display()

# COMMAND ----------

df05 = df04.withColumn("ACB",concat(col("App"),col("Category"))).withColumn("worker",lit("Abhra")).withColumn("new1",col("App"))

# COMMAND ----------

df05.display()

# COMMAND ----------

df05 = df05.withColumnRenamed("App","App Name")

# COMMAND ----------

df05.display()

# COMMAND ----------

df06 = df04.select("App")

# COMMAND ----------

df06.display()

# COMMAND ----------

df07 = df04.selectExpr('cast(Rating as Integer) as INTrating')

# COMMAND ----------

df07.display()

# COMMAND ----------

dfsort = df04.sort(col("Rating").desc())
dforderBy = df04.orderBy(col("Rating").desc())

# COMMAND ----------

dfsort.display()

# COMMAND ----------

df04.count()

# COMMAND ----------

df_dis = df04.distinct()

# COMMAND ----------

df_dis.count()

# COMMAND ----------

df_dropDup = df04.dropDuplicates(["Category","Genres"])
df_dropDup.display()

# COMMAND ----------

df_case = df_drop.withColumn("Category", when(col("Category")=="COMICS","MARVEL").when(col("Category")=="ART_AND_DESIGN","A&D").otherwise(col("Category")))

df_case.display()

# COMMAND ----------

df_gps = spark.read.option("header",True).schema(schemas).csv("/FileStore/gmde/googleplaystore.csv")
df_gps_ur = spark.read.option("header",True).option("inferschema",True).csv("/FileStore/gmde/googleplaystore_user_reviews.csv")


# COMMAND ----------

df_join = df_gps.join(df_gps_ur, df_gps.App == df_gps_ur.App)
df_join.display()

# COMMAND ----------

df_join_01 = df_gps.join(df_gps_ur, df_gps.App == df_gps_ur.App).select(df_gps['*'],df_gps_ur['Sentiment'])
df_join_01.display()

# COMMAND ----------

df_GB = df_join_01.groupBy("App").agg(avg("Rating").alias("Mean Rating"))
df_GB.display()
