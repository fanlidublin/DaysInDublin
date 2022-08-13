# Spark Exam Notes

Created: March 6, 2022
Created by: Anonymous
Tags: Study

---

> Exam Test 1
> 

---

**Cluster mode:**

![Untitled](Spark%20Exam%20Notes%20b7d268ca126f440abb8b2c415b8e8fa6/Untitled.png)

where the driver is inside the cluster manager, so the cluster manager is responsible for all spark application related processes.

**Client mode:**

![Untitled](Spark%20Exam%20Notes%20b7d268ca126f440abb8b2c415b8e8fa6/Untitled%201.png)

where the driver remains in the client machine, which means the client machine is responsible for maintain the driver process. The cluster manager is take care of the executors’ processes.

And from the pic we can see, the cluster manager is located on a node other than the client machine.

Note: In both modes, the cluster manager is typically on a separate node – not on the same host as the driver. It only runs on the same host as the driver in local execution mode.

**Local mode:**

there is no cluster, the Spark application is running on a single machine

---

For the Spark execution hierarchy: **tasks** are the smallest element. And **tasks** with narrow dependencies can be grouped into one stage. tasks are the unit of work done per partition.

(note that wide transformation cases a shuffle)

---

****Dynamic Partition Pruning****

(Dynamically injecting scan filters for join operations to limit the amount of data to be considered in a query is part of Dynamic Partition Pruning)

[Dynamic Partition Pruning in Spark 3.0 - DZone Big Data](https://dzone.com/articles/dynamic-partition-pruning-in-spark-30)

Partition pruning in Spark is a performance optimization that **limits** (**skips**) the number of files and partitions that Spark reads when querying. When partition filters are present, the catalyst optimizer pushes down the partition filters. The scan reads only the directories that match the partition filters, thus reducing disk I/O.

**During execution, under the hood:**

Spark takes this query and translates it into a digestible form, which we call the **logical plan**
 of the query. During this phase, Spark optimizes the logical plan by applying a set of transformations which are rule-based transformations such as column pruning, constant folding, filter push down. And only later on, it will get to the actual **physical planning**
 of the query. During the physical planning phase spark generates an executable plan. This plan distributes the computation across clusters of many machines.

![Untitled](Spark%20Exam%20Notes%20b7d268ca126f440abb8b2c415b8e8fa6/Untitled%202.png)

To summarize, in Apache sparks 3.0, a new optimization called dynamic partition pruning is implemented that works both at:

1. Logical planning level to find the dimensional filter and propagated across the join to the other side of the scan.
2. Physical level to wire it together in a way that this filter executes only once on the dimension side.
3. Then the results of the filter gets into reusing directly in the scan of the table. And with this two fold approach we can achieve significant speed ups in many queries in Spark.

Note there are lots of optimisation methods/functions on Spark 3.0, for example, here Dynamic partition pruning, and **adaptive query execution** *(optimizes query plans based on runtime statistics collected during query execution)*

**broadcast variables** is play a role for DPP during both logical and physical stages

---

DAG → directed acyclic graph, representing computational steps in Spark.

Hadoop → data need to be written and read from disk continuously

---

Spark execution hierarchy contains: Job, Stage and Task

where task is the deepest level (executors and slots facilitate the execution of tasks)

---

Dataset API is available in Scala but not Python. As it is used for object-oriented programming

provide type safety and support both structured and unstructured data

---

Spark partitions RDDs and distributes the partitions across multiple nodes

Spark UI is meant for inspecting the inner workings of Spark which ultimately helps understand, debug, and optimize Spark transactions

---

**Broadcast Variable:**

- are meant to be shared across the cluster, so available to all worker nodes
- can only be broadcast because they are small, and fit into memory
- cached on every machine in the cluster, precisely avoiding to have to be serialised with single task
- are immutable - never updated

---

`spark.default.parallelism`

`spark.sql.shuffle.partitions`

increase their values can → deal with large data on a single application 

The property `spark.dynamicAllocation.maxExecutors`is only in effect if dynamic allocation is enabled, using the `spark.dynamicAllocation.enabled`property. Dynamic allocation can be useful when to run multiple applications on the same cluster in parallel.

[Practical Spark Tips for Data Scientists](https://resources.experfy.com/bigdata-cloud/practical-spark-tips-for-data-scientists/#a-spark-sql-shuffle-partitions-and-spark-default-parallelism:~:text=a.%20spark.sql.shuffle.partitions%20and%20spark.default.parallelism:,sqlContext.setConf(%20%22spark.default.parallelism%22,%20800))

[Basics of Apache Spark Configuration Settings](https://towardsdatascience.com/basics-of-apache-spark-configuration-settings-ca4faff40d45)

---

A shuffle is a process that compares data across partitions, includes the process of sorting. 

Broadcast hash joins avoid shuffles and yield performance benefits if at least one of the two tables is small in size (<= 10 MB by default). Broadcast hash joins can avoid shuffles because instead of exchanging partitions between executors, they broadcast a small table to all executors that then perform the rest of the join operation locally.

[Spark Repartition & Coalesce - Explained](https://datanoon.com/blog/spark_repartition_coalesce/)

[Spark Architecture: Shuffle](https://0x0fff.com/spark-architecture-shuffle/)

---

Adaptive Query Execution (AQE)

- dynamically switch join strategies
    - dynamically coalescing shuffle partitions
    - dynamically optimizing skew join
- reoptimizes queries at materialization points
- is disabled in Spark needs to be enabled through the `spark.sql.adaptive.enabled`property
- applies only to queries that are not streaming queries and that contain at least one exchange (typically expressed through a join, aggregate, or window operator) or one subquery

---

Code block is intended to join DataFrame`itemsDf`with the larger DataFrame`transactionsDf`on column`itemId`

`transactionsDf.join(broadcast(itemsDf), "itemId")` this is the default in `DataFrame.join()`

Performance tuning: (broadcast operation is enabled by default)

`spark.sql.autoBroadcastJoinThreshold`property is set to 10 MB by default. If that property would be set to -1, then broadcast joining would be disabled

---

Code blocks efficiently converts DataFrame `transactionsDf` from 12 into 24 partitions

`transactionsDf.repartition(24)`

- coalesce() is used to reduce the number of partitions
- repartition() requires the numPartitions argument
- `transactionsDf.repartition(24, itemId")`is also correct

---

`transactionsDf.dropna("any")` remove all rows that have at least one missing value

`transactionsDf.dropna(how= ‘’, thresh=4)`

`na.drop()`

![Untitled](Spark%20Exam%20Notes%20b7d268ca126f440abb8b2c415b8e8fa6/Untitled%203.png)

---

`df.persist(StorageLevel.MEMORY_ONLY)` → all partitions that do not fit into memory will be recomputed when needed.

`df.cache()` by default is MEMORY_AND_DISK, means partitions that do not fit into memory are stored on disk.

`df.persist()` by default is also use MEMORY_AND_DISK.

---

![Untitled](Spark%20Exam%20Notes%20b7d268ca126f440abb8b2c415b8e8fa6/Untitled%204.png)

```python
from pyspark.sql.functions import explode

itemsAttributesDf = itemsDf.select("itemId", explode("attributes").alias("attribute"))
```

![Untitled](Spark%20Exam%20Notes%20b7d268ca126f440abb8b2c415b8e8fa6/Untitled%205.png)

- explode() is not a method of df, it should be used inside the select()
- split() is a method used to split strings into parts, not array or list
- explode can take a string “x” like the above code block shows, but also the following alternatives
    - `explode(col("x"))`
    - `explode(itemsDf.attributes)`
    - `explode(itemsDf['attributes'])`

---

**Read and Write**

`spark.read.parquet(path)`

`spark.read.format(”parquet”).schema(fileSchema).load(path)`

`spark.read.json(path)`

save the df as a csv, throws an error if fille already exists (it is the default mode!!!)

`df.write.format(”csv”).mode(”error”).save(path)`

`df.write.save()` by default save file as parquet (Spark), delta (Databricks)

mode(”ignore”) will not give an error if there is already a file

`df.write.format(”parquet”).partitionBy(”X”).save(”path”)`

write df to disk as parquet in location path, X for partition

`df.repartition(1).write.option(”sep”, “\t”).option(”nullValue”, “n/a”).csv(path)`

- write as a single file, by default every partition is written as a separate file
- use of option()
- .csv(path) can be updated as: `.save(path, format=”csv”)` as well

`df.write.format(”parquet”).mode(”overwrite”).option(”compression”, “snappy”).save(path)`

- DataFrameWriter → df.write
- mode
- `df.write.parquet` [https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.DataFrameWriter.parquet.html](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.DataFrameWriter.parquet.html)
- both ***parquet*** and ***save*** are the valid options for store as file

`df.write.format(”avro”).mode(”igore”).save(path)`

igore if a file already exists and not going to replace the file, not throw any error

- append
- overwrite
- ignore
- error or errorifexists

`df.write.format("parquet").option("mode", "append").save(path)`

`df = spark.read.load("data/transactions.csv", sep=";", format="csv", header=True, inferSchema=True)`

- by default Spark does not infer the schema of csv

`spark.read.format(”binaryFile”).option(”pathGlobFilter”, “*.png”).load(path)`

- deal with binary files, i.e. images
- pathGlobFilter to filter files by name
- load is correct, where open(path) does not exist

`spark.read.format(”csv”).option(”header”, True).load(path)`

![Untitled](Spark%20Exam%20Notes%20b7d268ca126f440abb8b2c415b8e8fa6/Untitled%206.png)

---

`df.filter(col("x") == 25).take(5)`

- collect() doesn’t take argument
- toLocalIterator() is take a boolean parameter for ‘prefectchPartitions’
- head(5) works the same

---

The following code all works:

```python
df.withColumn("X", pow(col("Y"), lit(2)))
df.withColumn("X", pow(col("Y"), 2))
df.withColumn("X", pow("Y", lit(2)))
```

---

- where() and filter() are equivalent
- where() can take a string argument
- where() returns a new df

---

array_contains()

`itemsDf.filter("array_contains(attributes, 'cozy')").select("itemId", explode("attributes"))`

or:

`**pyspark.sql.functions**`

`itemsDf.filter(array_contains("attributes", "cozy")).select("itemId", explode("attributes"))`

---

`df.withColumnRenamed(”String_old”, “String_new”)`

`withColumn`:

- requires 2 arguments
    - new column name
    - `Column` object

`df.withColumn(”new_column”, from_unixtime(”time_col”, format=”dd/MM/yyyy”))`

(new column with the unix epoch timestamps)

---

`df.sort(”column_x”, ascending=False)`

`df.sort(desc_nulls_last(”column_x”))`

- all missing values last

`df.sort(col(”x”))`

`df.sort(asc(”x”))`

`df.sort(asc(col(”x”)))`

`df.sort(df.value)`

`df.sort(sf.value.asc())`

note: ascending is default

orderBy is an alias of sort 

---

`df1.join(df2, df1.x == df2.x, “outer”)`

`df1.join(broadcast(df2), df1.x == df2.x)`

(small df2 is sent to all executors where it is joined with df1)

---

`repartition(numPartitions, *cols)`

- always trigger shuffle
- can do both increase and decrease
- basically any arguments after numPartitions are interpreted as column, so no brackets
    - `repartition(10000, “col_1”, “col_2”)`

`coalesce()`

- coalesce doesn’t have the shuffle option
- when we have no idea how many partitions a df has, we cannot safely use it
- only to decrease the size

---

`df.drop(”x1”, “x2”, “x3”)`

`df.drop(*col)` → all arguements (strings) are treated as column names, list is not correct

note if x1 doesn’t in the df, then does not have any effect, x2 and x3 can be dropped.

count() is an action, select() is a transaction

`df.select([”x1”, “x2”, “x3”])`

- note the difference between drop and select

`spark.createDataFrame([(”summer”, 4.5), (”winter”, 7.5)], [”season”, “wind_speed_ms”])`

note the difference between pandas df (use the dictionary and kv mapping), can directly transfer

`spark.createDataFrame(pands_df)`

`df.select((col(”x1”).between(20, 30)) & (col(”x2”)==2))`

![Untitled](Spark%20Exam%20Notes%20b7d268ca126f440abb8b2c415b8e8fa6/Untitled%207.png)

note the select here is going to give the boolean type as return, where filter | where give the df data results

---

`df.dropDuplicates(subset=[”X”, “Y”])`

`df.withColumn(”add_column_name”, split(”some_column”, “ ”))`

`df.filter(size(”col_x”)>3)`

- difference between: count(size on a group), size (return the number of elelments in an array on a per-row basis)
- difference between: filter, select (filter give the orign filtered data, the select give boolean)

---

`my_func_udf = udf(some_code_function)`

`df.withColumn(”new_col”, my_func_udf(”col_use”))`

note: usually pass into the return type, but here string is the default expected type, if we want intger:

`my_func_udf = udf(some_code_function, IntegerType())`

---

`spark.udf.register(”give_it_a_func_name”, python_fuct, LongType())`

![Untitled](Spark%20Exam%20Notes%20b7d268ca126f440abb8b2c415b8e8fa6/Untitled%208.png)

---

`df.sample(withReplacement=None, fraction=None, seed=None)`

- withReplacement: if True, a row appear more than once
- 150 out of 1000, then fraction = 0.15
- Duplicates may be returned,  withReplacement = True

---

contains(), isin()

Get a df with every 2nd row in the old_df, only columns x1, x2 required

`df.filter(col(”id”) % 2 == 0).select(”x1”, “x2”)`

---

`df.printSchema()`

`print(df.schema)`

distinct(), and there is NO!! unique() function

lit(1), add column with constant value

---

> Exam Test 2
> 

---

Job, Stage, Task

- A job is a sequence of stages, consists of one or multiple stages
- Slot are not part of execution hierarchy, tasks are the lowers layer

---

Executor communicate with driver directly

Slots are made avaiable in accordance with 

- how many cores per executor `spark.executor.cores`
- how many cpus per task `spark.task.cpus`

a slot can span multiple cores. If a task would require multiple cores, it would have to be executed through a slot that spans multiple cores. In Spark documentation, "core" is often used interchangeably with "thread", although "thread" is the more accurate word. A single physical core may be able to make multiple threads available. So, it is better to say that a slot can span multiple threads.

Spark store data on disk in multiple partitions, not slots

---

![Untitled](Spark%20Exam%20Notes%20b7d268ca126f440abb8b2c415b8e8fa6/Untitled%209.png)

Spark uses the catalog to resolve the unresolved logical plan, but not the optimized logical plan. Once the unresolved logical plan is resolved, it is then optimized using the Catalyst Optimizer. The optimized logical plan is the input for physical planning.

The catalog stores metadata, such as a list of names of columns, data types, functions, and databases. Spark consults the catalog for resolving the references in a logical plan at the beginning of the conversion of the query into an execution plan. The result is then an optimized logical plan.

Spark considers multiple physical plans on which it performs a cost analysis and selects the final physical plan in accordance with the lowest-cost outcome of that analysis. That final physical plan is then executed by Spark.

Regardless of whether DataFrame API or SQL API are used, the physical plan are the same.

[Spark's Logical and Physical plans ... When, Why, How and Beyond.](https://medium.com/datalex/sparks-logical-and-physical-plans-when-why-how-and-beyond-8cd1947b605a)

**DAGs can be decomposed into tasks that are executed in parallel.**

(DAGs-Directed Acyclic Graph, follow Spark's workload hierarchy. They comprise a job, which consists of stages, which consists of tasks. Some of those tasks may be executed in parallel, since they do not depend on each other.)

DAGs represent the execution plan in Spark and as such are lazily executed when the driver requests the data processed in the DAG.

---

Spark driver transforms operations into DAG computations itself.

Always a single driver per application, but one or more executors.

Executors precess partitions in an optimized, distributed fashion.

Slots are located inside executors, and executors are launched by the cluster manager at the start of the Spark application.

If data is cached, it is cached directly in the executors and not in a separate thread on the worker node.

There is only one Spark driver per application and it is hosted separately from the executors.

---

`df.foreach()`

The intention of foreach() is to apply code to each element of a DataFrame to update accumulator variables or write the elements to external storage. The process does not return an RDD - it is an action!

first(), count() and show() are all actions

Execution is triggered by actions only.

Lineage enable lazy evaluation.

Predicate pushdown means that, for example, Spark will execute filters as early in the process as possible so that it deals with the least possible amount of data in subsequent transformations, resulting in a performance improvements.

Accumulators are only updated when the query that refers to the is actually executed. In other words, they are not updated if the query is not (yet) executed due to lazy evaluation. 

Due to lazy evaluation, Spark will fail a job only during execution, but not during definition.

---

Between transformations, DataFrames are immutable. Given that Spark also records the lineage, Spark can reproduce any DataFrame in case of failure. These two aspects are the key to understanding fault tolerance in Spark.

RDD stands for Resilient Distributed Dataset and it is at the core of Spark.

For supporting recovery in case of worker failures, Spark provides "_2", "_3", and so on, storage level options, for example  MEMORY_AND_DISK_2. These storage levels are specifically designed to keep duplicates of the data on multiple nodes. This saves time in case of a worker fault, since a copy of the data can be used immediately, vs. having to recompute it first.

Spark is fault-tolerant by design.

---

Spark memory usage can be divided into:

- execution
- storage

Spark garbage collection runs faster on fewer big objects than many small objects

Serialization reduces the memory footprint, but may impact performance in a negative way

Reserved system memory is separate from Spark memory, reserved memory stores Spark’s internal objects

---

Spark's DataFrames are built on top of RDDs which are immutable. So, DataFrames are immutable as well.

Data in DataFrames is organized into named columns. This is also what distinguishes them from RDDs, which are much more flexible with regards to how data is organized.

---

The default value of the applicable property `spark.sql.shuffle.partitions` is 200.

The maximum number of tasks that an executor can process in parallel depends on both properties `spark.task.cpus`and `spark.executor.cores`. This is because the available number of slots is calculated by dividing the number of cores per executor by the number of cpus per task.

---

`df.coalesce(n)` is a narrow transaformation, and avoid data FULL shuffle, but will do some data shuffle if needed. As a general rule, it will reduce the number of partitions with the very least movement of data possible.

[Spark - repartition() vs coalesce()](https://stackoverflow.com/questions/31610971/spark-repartition-vs-coalesce)

The `repartition`operation will fully shuffle the DataFrame.

---

A wide transformation includes a shuffle, meaning that an input partition maps to one or more output partitions. This is expensive and causes traffic across the cluster. With the **select()** operation however, you pass commands to Spark that tell Spark to perform an operation on a specific slice of any partition. For this, Spark does not need to exchange data across partitions, each partition can be worked on independently. Thus, you do not cause a wide transformation.

**repartition():** When you repartition a DataFrame, you redefine partition boundaries. Data will flow across your cluster and end up in different partitions after the repartitioning is completed. This is known as a shuffle and, in turn, is classified as a wide transformation.

When you aggregate, you may compare and summarize data across partitions. In the process, data are exchanged across the cluster, and newly formed output partitions depend on one or more input partitions. This is a typical characteristic of a shuffle, meaning that the **aggregate()** operation may classify as a wide transformation.

**join():** Joining multiple DataFrames usually means that large amounts of data are exchanged across the cluster, as new partitions are formed.

**sort():** When sorting, Spark needs to compare many rows across all partitions to each other.

---

**Data Skew:**

Spark does not automatically optimize **skew joins** by default

- Automatic skew join optimization is a feature of Adaptive Query Execution (AQE). By default, AQE is disabled in Spark. To enable it, Spark's `spark.sql.adaptive.enabled`configuration option needs to be set to true instead of leaving it at the default false.
- Also, `spark.sql.adaptive.skewJoin.enabled` needs to be turn on as True, which it is by default
- When skew join optimization is enabled, Spark recognizes skew joins and optimizes them by splitting the bigger partitions into smaller partitions which leads to performance increases.

Joining keys that contain **null values** is of particular concern with regard to data skew

- In real-world applications, a table may contain a great number of records that do not have a value assigned to the column used as a join key. During the join, the data is at risk of being heavily skewed. This is because all records with a null-value join key are then evaluated as a single large partition
- Spark specifically does not handle this automatically. However, there are several strategies to mitigate this problem like discarding null values temporarily, only to merge them back later

In **skewed DataFrames**, the largest and the smallest partition consume very different amounts of memory

- In fact, having very different partition sizes is the very definition of skew.
- Skew can degrade Spark performance because the largest partition occupies a single executor for a long time. This blocks a Spark job and is an inefficient use of resources, since other executors that processed smaller partitions need to idle until the large partition is processed.

Salting can resolve data skew

- The purpose of salting is to provide Spark with an opportunity to repartition data into partitions of similar size, based on a salted partitioning key.
- A salted partitioning key typically is a column that consists of uniformly distributed random numbers. The number of unique entries in the partitioning key column should match the number of your desired number of partitions. After repartitioning by the salted key, all partitions should have roughly the same size.

Broadcast joins are a viable way to increase join performance for skewed data over sort-merge joins

- Broadcast joins can indeed help increase join performance for skewed data, under some conditions. One of the DataFrames to be joined needs to be small enough to fit into each executor's memory, along a partition from the other DataFrame. If this is the case, a broadcast join increases join performance over a sort-merge join.
    - A sort-merge join with skewed data involves excessive shuffling. During shuffling, data is sent around the cluster, ultimately slowing down the Spark application. For skewed data, the amount of data, and thus the slowdown, is particularly big.
    - Broadcast joins, however, help reduce shuffling data. The smaller table is directly stored on all executors, eliminating a great amount of network traffic, ultimately increasing join performance relative to the sort-merge join.
- `spark.sql.autoBroadcastJoinThreshold` it may make sense to manually adjust the default value which is 10MB

---

Accumulator

- when Spark tries to rerun a failed action that includes an accumulator, it will only update the accumulator if the action succeeded.
- Although accumulators behave like write-only variables towards the executors and can only be read by the driver, they are not immutable.
- broadcast variables are used to pass around lookup tables across the cluster.
- accumulators are instantiated via the `accumulator(n)`method of the `sparkContext`, for example: `counter = spark.sparkContext.accumulator(0)`.

---

`df.select(explode(”x”).alias(”new_x”)).filter(col(”new_x”).contains(”lifan”))`

- the use of explode() is a func
- contains can be called by a Col object

---

Caching means storing a copy of a partition on an executor, so it can be accessed quicker by subsequent operations, instead of having to be recalculated. It is a lazy evaluated method. 

---

`df.sort(”col_1”, des(”col_2”))`

- when the question ask about sorting based on 2 columns, any option that sorts the entire DataFrame (through chaining sort statements) will not work. The two columns need to be passed through the same call to sort() or orderBy().

`spark.createDataFrame([("red",), ("blue",), ("green",)], ["color"])`

`df.select("storeId", "predError").collect()`

- collect() is a method of DF, not spark session

---

Store df on 2 different executors, utilizing the executors’ memory as much as possible, but not writing anything to disk.

`from pyspark import StorageLevel
df.persist(StorageLevel.MEMORY_ONLY_2).count()`

- Only persist() can take different storage levels
- persist() is evaluated lazily, an action required if actually doing things
- Since the data need to be duplicated across two executors, **_2** needs to be appended to the storage level.

`df.cache()`

- store df in executor memory, if insufficient memory, serializes it and saves it to disk
- by default, cache() doing the above thing, which is MEMORY_AND_DISK
- persist() can achieve the same behavior, but not with the MEMORY_ONLY level which provided in the question option

---

PySpark Column expression

- col(”x”)
- df.x
- “x”

Code block returns a copy of df where the column x has been converted to string type:

`df.withColumn(”new_x”, col(”x”).cast(”string”))`

- cast() is a method of the Column class
- Column.astype() also works

Code block returns a one-column df where the x is converted to string type

`df.select(col(”x”).cast(StringType()))`

- can use cast(”string”) as well, like above

---

`df_dates = df_dates.withColumn(”date”, **to_timestamp**(”date”, “dd/NN/yyyy HH:mm:ss”))`

`df1.union(df2).distinct()`

Code list all items in column ‘attributes’ orderd by the number of times these items occur, from most of least ofter

![Untitled](Spark%20Exam%20Notes%20b7d268ca126f440abb8b2c415b8e8fa6/Untitled%2010.png)

```
df = df.select(explode(col('attributes')))
df = df.groupby('col').count()
df = df.sort('count',ascending=False).select('col')
```

---

`spark.conf.set("spark.sql.shuffle.partitions", 100)`

- conf is part of SparkSession

`spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 20)`

- the above set make no sense, as the default is 10 MB, Spark will only broadcast df that are much smaller than the 20 and even smaller than the default value
- something like: `spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 5)`make sense

---

`itemsDf.select(length(regexp_replace(lower(col("itemName")), "a|e|i|o|u|\s", "")).alias("consonant_ct"))`

- size works on arrays
- length works on strings

---

`df.collect()` sends all data in a df from ***executors*** to the ***driver***

---

`df1.join(df2, df1.productId==df2.itemId, how='inner').filter(~isnull(col('value'))).count()`

---

`df.filter(col('predError').isin([3, 6])).count()`

- note there is no ‘in’ method

---

```
df = spark.read.json(jsonPath)
df.createOrReplaceTempView("importedDf")
spark.sql("SELECT * FROM df WHERE productId != 3")
```

- note read.json is the correct way of loading json
- and use load(), not path()

---

> Exam Test 3
> 

---

`df.sample(fraction=0.1, seed=123)`

- to ensure not return duplicates, always leave withReplacement = False, default
- If replacement is True, means you put the balls back to bucket, there will be duplicates

`df.groupby('productId').agg(max('value').alias('highest'), min('value').alias('lowest'))`

`df.groupby(col('productId')).agg(max(col('value')).alias("highest"), min(col('value')).alias("lowest"))`

`df.write.partitionBy(”StoreId”).parquet(filePath)`

`spark.read.json(filePath)` 

- is correct
- [spark.read](http://spark.read) is a way to access Spark’s DataFrameReader
- doesn’t have any path() method

`spark.read.option(”mergeSchema”, “true”).parquet(filePath)`

- additional columns will be added in
- same columns name with different column type will result the mergeSchema to fail
- can update as `spark.read.parquet(filePath, mergeSchema = ‘True’)` the same

`df.filter(col(”supplier”).contains(”Sports”)).select(”itemName”, explode(”attributes”))`

**Narrow, wide transformation**

- A narrow transformation is an operation in which no data is exchanged across the cluster, since they do not require any data from outside of the partition they are applied on. i.e. filter, drop, coalesce.
- Wide transformation require data exchange across patitions
- Type conversion has nothing to do with narrow transformations in Spark
- A RDD can be described as a collection of partitions. As in narrow transformation, no data exchange between partitions, thus no data exchange between RDDs
- Any transformation will result in a new RDD being created. Since RDDs are immutable, a new RDD needs to be created to reflect the change caused by the transformation

 **Job, Staging and Task**

- tasks in a stage may be executed by multiple machines at the same time
- stages are senquential, stage A → stage B
- stages not contain wide transformation. Shuffling typically terminates a stage, as data needs to be exchanged across the cluster. Causing partitions to change and rearrange, make it impossible to perform tasks in parallel on the same dataset
- Tasks get assigned to the executors by the driver, executors take the tasks that they were assigned to by the driver. run them over partitions, and report the outcomes back to the driver
- A partition is a collection of rows, a task processes a specific partition
- Driver does not send anything to the executors in response to a transformation, as transformations are evaluated lazily. driver send tasks to executors only in response to actions
- Executors have one or more slots to process tasks and each slot can be assigned a task

The whole point of client mode is that the driver is outside the cluster and not associated with the resource that manages the cluster (the machine that runs the cluster manager).

Standalone mode uses only a single executor per worker per application.

**Shuffle**

- Intermediate result during a shuffle are written to disk
- Shuffle is a wide transformation, not action
- Involve multiple partitions
- It is also lazy

**Action & Transformation**

- Actions can trigger AQE (adaptive query execution) which optimaze queries at runtime.
- Transformation changes the data and, since RDDs are immutable, generate new RDDs along the way
- Actions do not generate RDDs
- If an operation returns a DF, Dataset or RDD, then it is a Transformation
- Action send the result to driver
- Transformation not send result back to driver, they produce RDDs that remain on the worker nodes

**Clsuter manager**

- In order for the driver to contact the cluster manager, the driver launches a SparkContext. The driver then asks the cluster manager for resources to launch executors.
- The cluster manager exists even in standalone mode. Remember, standalone mode is an easy means to deploy Spark across a whole cluster, with some limitations. For example, in standalone mode, no other frameworks can run in parallel with Spark.
- Driver transforms joibs into DAGs
- Cluster managers do not work on partitions directly. Their job is to coordinate cluster resources so that they can be requested by and allocated to Spark driver

Execution modes

- Client
- Cluster
- Local

Deployment modes

- Standalone
- YARN
- Mesos
- K8s

A stage boundary is commonly established by a shuffle, for example caused by a wide transformation.

**Executors**

- Executors stop upon application completion by defaylt, only persist during the lifetime of an application. However, when dynamic resource allocation enabled, executors are terminated when they are idle, independent of whether the application has been completed or not
- Only serve specific on application
- Each node can host one or more executors
- Executors store data in memory or disk
- Executors are launched by the cluster manager, then communicate with driver

**Partitions**

- 200 is the default value for the Spark property `spark.sql.shuffle.partitions`
- coalesce() be used to decrease the number of partitions. While coalesce() avoids a full shuffle, it may still cause a partial shuffle, resulting in data exchange between executors.
- have the number of partitions equal to the number of executors is normal ideal
- Data skew means that data is distributed unevenly over the partitions of a dataset. Low skew therefore means that data is distributed evenly. A situation indicative of low skew may be when all executors finish processing their partitions in the same timeframe. High skew may be indicated by some executors taking much longer to finish their partitions than others

**Accumulator**

- Accumulator values can only be read by the driver, but not by executors
- Not able to use for coordinating workloads between executors
- Typical use case is to report data for debugging purposes
    - For example, count values that match a specific condition in a UDF for debugging
- Though PySpark only support numeric values, we can define custom types via AccumlatorParam interface for the accumulators
- Accumulator also obey lazy evaluation
- Under certain conditions accumulator can run for each task more than once.