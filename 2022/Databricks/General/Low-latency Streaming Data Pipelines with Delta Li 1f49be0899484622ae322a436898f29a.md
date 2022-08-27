# Low-latency Streaming Data Pipelines with Delta Live Tables and Apache Kafka

Tags: Databricks
URL: https://www.databricks.com/blog/2022/08/09/low-latency-streaming-data-pipelines-with-delta-live-tables-and-apache-kafka.html

### DLT - Delta Live Tables

DLT  is the first ETL framework that uses a simple declarative approach for creating reliable data pipelines and fully manages the underlying infrastructure at scale for batch and streaming data. Many use cases require actionable insights derived from near real-time data. Delta Live Tables enables **low-latency streaming data pipelines** to support such use cases with low latencies by directly ingesting data from event buses like Kafka, AWS Kinesis, Confluent Cloud, Amazon MSK, Azure event hub.

### Streaming platforms

Event buses or message buses decouple message producers from consumers. A popular streaming use case is the collection of click-through data from users navigating a website where every user interaction is stored as an event in Apache Kafka. The event stream from Kafka is then used for real-time streaming data analytics. Multiple message consumers can read the same data from Kafka and use the data to learn about audience interests, conversion rates, and bounce reasons. The real-time, streaming event data from the user interactions often also needs to be correlated with actual purchases stored in a billing database.

### Apache Kafka

Kafka is a popular open source event bus. Kafka uses the concept of a topic, an append-only distributed log of events where messages are buffered for a certain amount of time. Although messages in Kafka are not deleted once they are consumed, they are also not stored indefinitely. The message retention for Kafka can be configured per topic and defaults to 7 days. Expired messages will be deleted eventually.

### Streaming data popelines

- In a data flow pipeline, Delta Live Tables and their dependencies can be declared with a standard SQL Create Table As Select (CTAS) statement and the DLT keyword “live.”
- When developing DLT with Python, the `@dlt.table` decorator is used to create a Delta Live Table. To ensure the data quality in a pipeline, DLT uses **`Expectations`** which are simple SQL constraints clauses that define the pipeline’s behavior with invalid records.
- Since streaming workloads often come with unpredictable data volumes, Databricks employs `enhanced autoscaling` for data flow pipelines to minimize the overall end-to-end latency while reducing cost by shutting down unnecessary infrastructure.
- DLT v.s. Streaming DLT
    - DLT are fully recomputed, in the right order, exactly once for each pipeline run.
    - Streaming DLT are stateful, incrementally computed and only process data that has been added since the last pipeline run. If the query which defines a streaming live tables changes, new data will be processed based on the new query but existing data is not recomputed. Streaming live tables always use a streaming source and only work over append-only streams, such as Kafka, Kinesis, or Auto Loader. Streaming DLTs are based on top of Spark Structured Streaming.
    - We can chain multiple streaming pipelines, for example, workloads with very large data volume and low latency requirements.

### Direct Ingestion from Streaming Engines

Delta Live Tables written in Python can directly ingest data from an event bus like Kafka using Spark Structured Streaming. We can set a short retention period for the Kafka topic to avoid compliance issues, reduce costs and then benefit from the cheap, elastic and governable storage that Delta provides.

- Ingesting the data as is to a bronze (raw) table and avoid complex transformations that could drop important data.
- Like any Delta Table the bronze table will retain the history and allow to perform GDPR and other compliance tasks.

![I*ngest streaming data from Apache Kafka*](Low-latency%20Streaming%20Data%20Pipelines%20with%20Delta%20Li%201f49be0899484622ae322a436898f29a/Untitled.png)

I*ngest streaming data from Apache Kafka*

There is no special attribute to mark streaming DLTs in Python; simply use `spark.readStream()`
to access the stream.

```python
import dlt
from pyspark.sql.functions import *
from pyspark.sql.types import *

TOPIC = "tracker-events"
KAFKA_BROKER = spark.conf.get("KAFKA_SERVER")
# subscribe to TOPIC at KAFKA_BROKER
raw_kafka_events = (spark.readStream
    .format("kafka")
    .option("subscribe", TOPIC)
    .option("kafka.bootstrap.servers", KAFKA_BROKER)
    .option("startingOffsets", "earliest")
    .load()
    )

@dlt.table(table_properties={"pipelines.reset.allowed":"false"})
def kafka_bronze():
  return raw_kafka_events
```

- pipelines.reset.allowed
    - Event buses typically expire messages after a certain period of time, whereas Delta is designed for infinite retention
    - This could lead to the effect that source data on Kafka has already been deleted when running a full refresh for a DLT pipeline. In this case, not all historic data could be backfilled from the messaging platform, and data would be missing in DLT tables.
    - The the attribute to false can prevents full refreshes to the tables (which potentially loss data), but does not prevent incremental writes to the tables or new data from flowing into the table.
- Checkpointing missing
    - In Spark Structured Streaming checkpointing is required to persist progress information about what data has been successfully processed and upon failure, this metadata is used to restart a failed query exactly where it left off.
    - Whereas checkpoints are necessary for failure recovery with exactly-once guarantees in Spark Structured Streaming, DLT handles state automatically without any manual configuration or explicit checkpointing required.
- Not allow SQL Python in one declaration notebook
- Schema mapping
    
    ```python
    event_schema = StructType([ \
        StructField("time", TimestampType(),True)      , \
        StructField("version", StringType(),True), \
        StructField("model", StringType(),True)     , \
        StructField("heart_bpm", IntegerType(),True), \
        StructField("kcal", IntegerType(),True)       \
      ])
    
    # temporary table, visible in pipeline but not in data browser, 
    # cannot be queried interactively
    @dlt.table(comment="real schema for Kakfa payload",
               temporary=True)
    
    def kafka_silver():
      return (
        # kafka streams are (timestamp,value)
        # value contains the kafka payload
            
        dlt.read_stream("kafka_bronze")
        .select(col("timestamp"),from_json(col("value")
        .cast("string"), event_schema).alias("event"))
        .select("timestamp", "event.*")     
      )
    ```
    

### Benefits

Reading streaming data in DLT directly from a message broker minimizes the architectural complexity and provides lower end-to-end latency since data is directly streamed from the messaging broker and no intermediary step is involved.

---

### Streaming Ingest with Cloud Object Store Intermediary

For some specific use cases you may want offload data from Apache Kafka, e.g., using a Kafka connector, and store your streaming data in a cloud object intermediary. In a Databricks workspace, the cloud vendor-specific object-store can then be mapped via the Databricks Files System (DBFS) as a cloud-independent folder. Auto Loader can ingest the files.

![Untitled](Low-latency%20Streaming%20Data%20Pipelines%20with%20Delta%20Li%201f49be0899484622ae322a436898f29a/Untitled%201.png)

```python
-- INGEST with Auto Loader
create or replace streaming live table raw
as select * FROM cloud_files("dbfs:/data/twitter", "json")
```

- Note that Auto Loader itself is a streaming data source and all newly arrived files will be processed exactly once, hence the streaming keyword for the raw table that indicates data is ingested incrementally to that table.
- Since offloading streaming data to a cloud object store introduces an additional step in your system architecture it will also increase the end-to-end latency and create additional storage costs. Keep in mind that the Kafka connector writing event data to the cloud object store needs to be managed, increasing operational complexity.
- Therefore Databricks recommends as a best practice to directly access event bus data from DLT using Spark Structured Streaming as discussed above.