# Packt - Azure Data Engineer Associate Certification Guide

Tags: Book

## Chapter 2 - Designing a Data Storage Structure

### Designing storage for efficient querying

- Storage layer
    - partitioning
    - data pruning
    - eventual consistency
- Application layer
    - data caching
    - application tuning (vary the sizes of containers, increase parallelism)
- Query layer
    - index
    - materialised views

<aside>
💡 Good partitions: those that can run parallel queries without requiring too many inter-partition data transfers. So, we divide the data in such a way that the data is spread out evenly and the related data is grouped together within the same partitions.

</aside>

- Strongly consistent
    - Ensure that all the data copies are updated before the user can perform any other operation
    - Query running on strongly consistent data stores tend to be slower as the storage system will ensure that all the write (to all the copies) are complete before the query can return
- Eventually consistent
    - Data in each of the copies get updated gradually over time
    - Query will rerun immediately after the first copy is done, and the rest of the updates to all the other copies happen asynchronously

### Create year, month, day partition

```python
dfDate = df.withColumn("date", to_timestamp(col("date"), "yyyyMMdd"))
					 .withColumn("year", date_format(col("date"), "yyyy""))
					 .withColumn("month", date_format(col("date"), "MM"))
					 .withColumn("day", date_format(col("date"), "dd"))

dfDate = dfDate.repartition("year", "month", "day")
dfDate.write.partitionBy("year", "month", "day").parquet(path)
```

### Folder structure

`{Region}/General/{SubjectMatter(s)}/In/{yyyy}/{mm}/{dd}/{hh}/`

`{Region}/General/{/{SubjectMatter(s)}/Out/{yyyy}/{mm}/{dd}/{hh}/`

`{Region}/Sensitive/{/{SubjectMatter(s)}/in/{yyyy}/{mm}/{dd}/{hh}/`

`{Region}/Sensitive/{/{SubjectMatter(s)}/Out/{yyyy}/{mm}/{dd}/{hh}/`

`{Region}/General/{/{SubjectMatter(s)}/Bad/{yyyy}/{mm}/{dd}/{hh}/`

`{Region}/Sensitive/{/{SubjectMatter(s)}/Bad/{yyyy}/{mm}/{dd}/{hh}/`

<aside>
💡 Do not put date folders at the beginning as it makes applying ACLs to every subfolder more tedious. Also, there are limits on the number of ACLs that can be applied, so there are chances of you running out of ACLs as time progresses. For example, the sensitive folder, we can easily apply all the security policies and ACLs at itself. The restrictions will automatically be inherited by all subfolders under it.

</aside>

### Distribution strategies

Synapse dedicated SQL pools - massively parallel processing (MPP) split query into 60 parallel queries. Distribution is a basic unit of processing and storage for a dedicated SQL pool.

- Round-robin tables
    - Data is serially distributed among all the distributions
    - Simplest and default
    - Quickest to load data, but not the best for queries that include joins
    - Use it for staging data or temporary data
- Hash tables
    - Hash func
    - Best for joins and aggregations, large tables
    - Column that is distinct and static as hash key can balance the data distribution among the partitions
- Replicated tables
    - Copied over to all the distributions
    - Small tables where the cost of copy are not experience
    - Lookup

### Data archive

- Hot
    - Data accessed frequently
    - Lowest access cost
    - Higher storage cost
- Cold
    - Occasionally
    - Slight older data for monthly reports maybe
    - Expect data to be stored for at least 30 days
- Archive
    - Long duration
    - Long-term backups, archival
    - Offline storage - Not able to access unless rehydrate that data from Archive to an Online tier
    - Cheapest storage option
    - Expect data to be stored for at least 180 days

## Chapter 3 - Designing a Partition Strategy

### Partition strategy for files

- Azure Blob storage
    - Account + container + blob as the partition key
    - When files reach the partition’s internal limit, automatically repatriation and rebalance
    - When data is large, the re-prcoess will affect or imapct the latency of the CRUD APIs
    - Add 3 digit hash value to filenames is good to cause data into multiple partitions
        - `New York/cabs/cab1234/customers/{XYZYYYYMMDD}`
        - XYZ
- ADLS Gen 2
    - Same as folder structure design

### Partition strategy for analytical workloads

- Horizontal partitioning, sharding
    - subsets of **rows** are stored in different data stores
    - shard key - partition key
        - application traffic to the data partitions is evenly distributed
        - key doesn’t change too often, static and widespread (the range of that key should neither be too small nor too large)
        - general rule - a key that can generate hundreds of partitions is good (not too few or too many)
        
        <aside>
        💡 Don't try to balance the data to be evenly distributed across partitions unless specifically required by your use case because usually, the most recent data will get accessed more than older data. Thus, the partitions with recent data will end up becoming bottlenecks due to high data access.
        
        </aside>
        
- Vertical partitioning
    - subsets of **columns** are stored in different data stores
    - queries select subsets of columns, no need to read entire rows
    - ideal for column-oriented data stores such as HBase, Cosmos DB
- Functional partitioning
    - similar to vertical partitions, except store entire tables or entities in different data stores
    - can be used to segregate data belong to different or, frequently used tables from infrequently used ones, read-write tables from read-only ones, sensitive data from general data

### Partition strategy for Azure Synapse

- Dedicated SQL pool support 3 types of tables
    - clustered column-store
    - clustered index
    - heap
- Performance improvement
    - loading data
    - filtering queries

## Chapter 4 - Designing the Serving Layer

### Star and Snowflake schemas

- Star schema
    - Fact table are usually of much higher volume than dim
    - Dim are not connected, independent of each other
    - Data is not normalised. Common to find data replicated in multiple tables
    - Optimized for BI queries. Usually very simple as it just has on level of joins
    - Queries can be faster due to lesser number of joins
- Snowflake schema
    - Dim tables are further split into their normalised forms
    - Referenced using foreign keys, which could causing multiple levels of hierarchy among the dim tables
    - Both BI and non-BI tools as end users
    - Data is normalised, thereby avoiding any redundant data
    - Dim can connect to each other
    - Data optimised for storage and integrity, but not speed
    - More complex, might not be the most preferred option for BI and reporting
    - Queries might be slower, due to the multi-level joins required
- Galaxy schema
    - More than on fact table, and dim tables are shared

### SCDs

- Dim tables that changes slowly over time and not at a regular cadence
- Design consideration
    - Should we keep track of the changes
        - If yes, how much of the history should we maintain
        - Or we can just overwrite the changes and ignore history
- SCD1
    - values are overwritten and no history is maintained
- SCD2
    - Maintain complete histories of changes by adding a new row
    - Use a flag, for example, “isActive”
        - Note surrogate keys are secondary row identification keys. They are added in all SCD2 cases because the primary identification key will not be unique anymore with newly added rows
    - Use version numbers
        - Use MAX(version) column to get the current values
    - Use data range
        - Periodic records
        - Filter the current value by using `EndDate = NULL` or `EndDate = 9999-12-31`
    - (Combination of these approaches are also reasonable to use)
- SCD3
    - Add the changed attribute as a new column, the new column to store the previous value
    - Only one version of historic data will be preserved
    - For example, if “City” column changed, “PrevCity” column will be added
- SCD4
    - Introduced for attributes that change relatively frequently
    - Split the fast-changing attributes of Dim into another smaller Dim
    - Reference the new Dim directly from the Fact
    - This helps when modification only require a smaller amount of data frequently instead of the complete row
- SCD6
    - Combination of 1, 2, 3
- Temporal data (temporal tables → system-versioned temporal tables)
    - Azure SQL
    - SQL Server
    
    ```sql
    CREATE TABLE Customer
    (
    	[customerId] INT NOT NULL PRIMARY KEY CLUSTERED,
    	[name] VARCHAR(100) NOT NULL,[address] VARCHAR(100) NOT NULL,
    	[email] VARCHAR (100) NOT NULL,[phone] VARCHAR(12) NOT NULL,
    	[validFrom] DATETIME2 GENERATED ALWAYS AS ROW START,
    	[validTo] DATETIME2 GENERATED ALWAYS AS ROW END,
    	PERIOD FOR SYSTEM_TIME (validFrom, validTo),
    )WITH (SYSTEM_VERSIONING = ON);
    ```
    
    - Start, end column, period for system_time
    - When create a temporal table, behind the scenes 2 tables get created
        - temporal table
        - history table
        - when data changes
            - the current values get persisted in the temporal table
            - the old values get moved into the history table with the end time updated to the current time stamp, with row no longer active
- Dimensional hierarchy
    - Group and organize the dimensional data at multiple levels
        - one-to-many
        - many-to-many
    - self-referencing or self-joins
    - always add the Parent key pointing to the Surrogate Key instead of the Business primary key. Because surrogate keys will be unique, and it will ensure that the dimensional hierarchy doesn't break when changes to the business key happens.
- Incremental loading
    - Watermarks
        - data source is a DB or relational table-based system
        - have a watermark table which store the info of lasted loaded record
        - stored procedure got triggered to update the watermark table when data load finish
        - use to identify (for example, `max(LastModifiedTime)`)the new set of records that need to be loaded
    - File timestamps
        - data source is a filesystem or blob
    - Partition data
        - data source is partitioned based on time
    - Folder structure
        - source is divided based on time
- Metastores in Synapse and Datrbicks
    - In-memory version → help jobs running on the JAV but not much further
    - External version → Hive, APIs to access it

## Chapter 5 - Implementing Physical Data Storage Structures

- Compression
- Partitioning
    - Folder structure
    - Horizontal partitioning or sharding
        - Dynamic in nature
        - Done after schemas are created
        - Usually performed regularly during data loading or during the data transformation
    - Vertical partitioning
        - During creating tables

### Sharding using Spark

- In-memory
    - `repartition()`
    - `coalesce()`
    - `repartitionByRange()`
- On-disk
    - when output the files → `partitionBy()`

### Distributions

- Hash
- Round-robin (staging tables, there is no good indexing to choose from)
- Replicated (Copy the complete table across all the nodes, for small but frequently accessed data)

### SQL dedicated pools → Index

- Clustered column-store indexing
    - default index
    - works best for large fact tables
    - column-based (provide high-level compression)
- Heap
    - staging tables
- Clustered index
    - row-based
    - looks, highly selective filters

### Data redundancy

Multiple copies of data at different locations

- Primary region redundancy
- Secondary region redundancy

Types

- Locally redundant storage (LRS)
- Zone redundant storage (ZRS)
- Geo redundant storage (GRS)
- Geo ZRS (GZRS)

## Chapter 6 - Implementing Logical Data Structures

### SCDs

- An data flow ingestion DimDriver example
    - new row added in
    - updated row got updated
        - new row added in with isActive = 1
        - all old rows updated to isActive = 0

![Untitled](Packt%20-%20Azure%20Data%20Engineer%20Associate%20Certificatio%20d3e75286646948f598eb625484464a82/Untitled.png)

### Logical folder structure

- Data pruning
    - Divide the data into partitions, ensure that the partitions are stored in different folder structures, then the queries can skip scanning the irrelevant partitions
- Partition switch and deletion
    - Dummy table for deletion, switch out the partition of the data
    - Add new partition needs to split the last partition into 2 partitions
        - the split won’t work if the partition contains data
        - so, temporarily swap out the last partition to a dummy table
        - after split, switch in the original data into the correct partition

### External Tables

- external data source
- external file format
- external table

## Chapter 7 - Implementing the Serving Layer

### Delivering data in a relational start schema

- Fact
    - Usually much higher in volume
    - Benefit from hash distribution
    - Clustered columnstore index
- Dim
    - Smaller
    - Benefit from using replicated tables
    - Also clustered columnstore index would be good
- Dimensional hierarchy
- Parquet
- SQL serverless pool is an on-demand service

## Chapter 8 - Ingesting and Transforming Data

### Spark

transformation with 3 different application programming interfaces (APIs)

- RDDs
    - immutable fault-tolerant collection of data objects that can be operated on in parallel by Spark
    - most fundamental data structure
- DataFrames
    - similar to tables in relational databases
    - like RDDs → immutable, redundant, distributed, but represent a higher form of data abstraction
    - contain schemas, columns and rows
- Datasets

### ADF

Schema transformations

- refer to the actions that result in changing the schema of the table or df
    - aggregate
    - derived column
    - select

Row transformations

- alter row
- filter
- sort

Multi-IO transformation

- conditional split
- join
- union

### Cleansing data

- Missing null value
    - substituting with default values
    - filter out null values
- Trimming input
    - trim(col)
- Standardizing values
    - for example → replace({salary}, ‘$’, ‘USD’)
- Handle outliers
- Remove duplicates or deduping

### Split data

- Conditional split
- New branch (copy the entire dataset fro a new execution flow)

### Extracting values from JSON

- Spark
    - spark.read.json(path)
    - with a pre-defined schema spark.read.schema(xxx).json(path)
- SQL
    - select xxx from openrowset(…)

### Encoding and decoding data

### Error handling for the transformation

### Normalizing and denormalizing values

- Flatten
- Pivot (turn the values in the column into multiple columns, with some aggregation func)
- Unpivot

## Chapter 9 - Designing and Developing a Batch Processing Solution

Batch process usually deals with larger amounts of data and takes more time to process compared to stream processing.

5 major components:

- storage system
- process engine
- orchestration tooling
- analytical data store
- BI tooling

For ingestion, need to consider

- Incremental data load
- SCDs
- Duplicate, missing data
- Late arriving (More reading on this!)
    - Drop the message: when the data is out of date, doesn’t add much value
    - Store the message and retry after some time: store the early-arriving fact rows in a staging table and try inserting this fact when in the next iteration, hoping that the dimension will have arrived by then. Repeat this process a pre-determined number of times before declaring failure
    - Insert a dummy record in the dimension table: If the corresponding dimension record doesn’t exist, just enter a dummy record in its place. Need to revisit all the dummy records and update them with real values once the dimension values arrive
    - If we have enough details about the dimension, we can inder the dimension row and insert the new derived dimension row with a new surrogate key

### Upsetting data

- update
- insert

### Regressing to a previous state

- When instructions fail or reach an inconsistent state then the entire transaction rolls back
- ADF provides options for checking consistency and setting limits for fault tolerance
- Delete activity for rollback (delete files, rows, so on)

### Azure batch

Azure service that can be sued to perform large-scale parallel batch processing. 

- Batch size configuration
- Resource scaling
    - manual
    - auto

Best practices

- Use private endpoints
- Create pools in virtual networks
- Create pools without public IP
- Limit remote access to pool nodes by configuring firewalls
- Encrypt data in transit by using https://
- Encrypt Batch data at rest by using secret keys
- Apply compliance and security policies

## Chapter 10 - Designing and Developing a Stream Processing Solution

- Major Components
    - Event ingestion service (event hubs, IoT hub, Kafka, etc.)
    - Stream process engine
    - Analytical data stores
    - Reporting systems
- Azure Event Hub
    - Distributed ingestion service
    - Buffer between the event producers and consumers
    - Decouples the event producers from the event consumers, helps the downstream stream components such as ASA or Spark to synchronously process the data
    - Fully managed PaaS service
    
    ![Untitled](Packt%20-%20Azure%20Data%20Engineer%20Associate%20Certificatio%20d3e75286646948f598eb625484464a82/Untitled%201.png)
    
    - Take inputs from 2 protocols
        - Hypertext Transfer Protocol (HTTP)
        - Advanced message Queuing Protocol (AMQP)
    - Then distributes the data into ***partitions***
        - Help horizontal scaling as they allow multiple consumers to read data in parallel
    - Event receivers, which are part of ***consumer groups***,, can subscribe to the partitions and read the event from there
    - Consumer groups are views of the event hub
        - access to different sets of streams or partitions
        - consumers access the partitions via their own consumer group
        - maintain state-like offsets in the stream, checkpointing info
        - the applications within a consumer group can independently process the data without worrying about other clients
- ASA
    - Azure’s primary stream processing engine
        - Process large volumes of data with minimal latencies
        - Stages
            1. Read from an ingestion service
            2. Process the data and generates insights
            3. Write the data into an analytical store
- Spark
    - Internally splits the incoming stream into micro-batches and process them
    - Example
        - connection string
        - readStream
        - json schema definition
        - stream handling to extract the body
        - window, output mode, checkpointing
    - Structured streaming
        - data continuously appended to unbounded table
        - batch processing syntax can be applied to write streaming queries to handle table-based transformations
        - structured streaming queries as incremental queries
        - runs at frequent intervals to continuously process the data
    - Write mode
        - Complete - entire output is written to the sink
        - Append - only new rows from the last time
        - Update - only the rows that have changed are updated
    - Monitor Spark metrics
        - input rate
        - processing rate
        - batch duration
- Process time series data
    - Data recorded continuously over time
    - Appended heavily
    - Timestamps
        - Event time
        - Processing time
    - Windowed aggregates
        - Since time series events are unbounded events, no well-defined end time, necessary to process the event in small batches
    - Checkpointing or Watermarking
        - Keep track of the last event or timestamp that was processed
        - Ensure we start from the previously stopped place and don’t miss out any events
    - Replay data
        - Re-process older events, previous offset location
- Windowed aggregates
    - Tumbling windows
        - non-overlapping
        - same size
    - Hopping windows
        - fixed overlap
        - same size
    - Sliding windows
        - fixed size
        - only forward when either event add or remove
    - Session windows
        - pre-defined max size
        - grab events as many as possible
        - if no event, timeout and close
    - Snapshot windows
        - not really window tech
        - used to get a snapshot of the event at a particular time
- Configure checkpoints
- Replay archived stream data (event hub default 7 days)
- Transformation
    - COUNT(DISTINCT xxx)
    - CAST(xxx AS FLOAT)
    - WHERE xxx LIKE ‘%123%’
- Schema drift
    - Azure schema register
        - register
        - retrieve
    - Delta lake schema evolution
        - .option(”mergeSchmea”, “true”)
- Partitions
    - distribute incoming events into multiple streams
    - within one partition
    - across partitions
- Scaling resources
    - Partitions
    - Auto-inflate
        - auto scale up feature
        - as the usage increases, added more throughput units to the instance
        

## Chapter 11 - Managing batches and Pipelines

- Azure function - serverless
    - only one trigger associated with it
- Failed batch loads
    - Pool errors
        - Insufficient quota
        - Insufficient resource in VNet
        - Short timeouts
    - Node errors
        - Start task failures
        - Application download failures
        - Nodes going into a bad state
    - Job errors
    - Task errors
- ADF validation
    - Validation task
    - Get metadata
    - If condition
- ADF trigger
    - schedule
    - tumbling window
    - event-based
        - built-in event, such as files being created in Blob or ADLS
    - custom
        - trigger pipelines based on events from Azure event grid. listen to topics in azure event grid and trigger pipelines based on certain messages or event occurring in the topic
- Integration Runtime
    - Azure IR
        - Default
        - Connect data store and compute service across public endpoints
        - Copy data between Azure-hosted services
        - Also support connect data stores using private links
    - Self-hosted IR
        - Copy data between on-premises clusters and Azure services
        - On the machines or VMs on the on-premises private network to install a self-hosted IR
    - SSIS IR
        - Used for SSIS lift and shift uses cases

## Chapter 12 - Designing Security for Data Policies and Standards

- Sensitive information handling
    - Data masking
    - Row and column level security
    - Role-based access
    - Access-controlled lists
    - Enable encryption
- Encryption in transit
    - Secure sockets layer (SSL)
    - Transport layer security (TLS)
- RBAC (Role-Based Access Control)
    - Security principal
        - user, group or managed identity (service accounts whose life cycle is completely managed by Azure) created within AAD
        - as “who”
        - it is the entity that we request permission for
    - Role
        - define what actions can be performed by a principal
        - pre-defined roles
    - Scope
        - where the role needs to be applied
            - resource group? or container in a storage account? or multiple containers? etc.
- ACLs (Access Control Lists)
    - while RBAC provides coarse-grained access
    - ACLs offer more fine-grained access

![Untitled](Packt%20-%20Azure%20Data%20Engineer%20Associate%20Certificatio%20d3e75286646948f598eb625484464a82/Untitled%202.png)

(Azure gives precedence to RBAC)

- Shared key
    - gives admin-like access
- Shared Access Signature (SAS token)
    - define what actions are allowed

Note: both these 2 methods will override RBAC and ACLs. Recommendation is to use AAD RBAC and ACLs wherever possible

- Row and column level security
    - Row level
        - create function similar to where statement
        - create security policy by passing the function
    - Column level
        - similar to data mask
        - but instead of masking the column, restrict the column access completely to unauthorized users
- Data retention policy
    - Scheduled data deletion
    - Data purging - remove data as per business requirements
- Azure Active Directory (AAD)
    - Azure’s identity and access management service
    - Manage users, groups, service principals, and so on
- Managed identities
    - identities that are assigned to instance of Azure services such a VMs, Synapse, SQL DB, etc.
    - life cycle automatically managed by AAD
    - managed identity can be used by the instance to authenticate itself with AAD
- Key valut
    - Key
    - Secrets
    - Certificate
- Secure endpoints
    - public endpoint
        - default way of creating Azure services, where the service can be accessed from a public IP address
        - any resources we created in Azure without configuring a VNet will go into public endpoint category
    - private endpoint
        - more secure with private IP
        - private link - make azure service available only on certain private IP addresses within VNets
        - no one outside the VNets will even aware the existence of such a service

## Chapter 13 - Monitoring Data Storage and Data Processing

- Azure monitor
    - Record 2 types of data
        - metrics
        - logs
    - Azure log analytics workspaces

## Chapter 14 - Optimizing and Troubleshooting Data Storage and Data Processing

- Compact small files
    - wildcard file path
    - sink → copy behavior → merge files
    - incrementally loading
    - bin packing(Delta lake)
        - delta.autoOptimize.optimizeWrite = true
        - delta.autoOptimize.autoCompact = true
- UDFs
- Handle skews in data
    - storage level
        - Better distribution or partition strategy that would balance the data evenly
        - Add a second distribution key
        - Randomize the data and then use the round-robin technique to distribute the data evenly
    - compute level
        - improve the query plan by enabling statistics
            - query engines such as the Synapse SQL engine, which uses a cost-based optimizer, will utilize statistics to generate the most optimal plan based on the cost associated with each plan
            - optimizer can identify data skews and automatically apply the appropriate optimizations in place to handle skew
        - ignore the outlier data if not significant
- Handle data spills
    - Refers to the process where compute engine usable to hold the required data in memory and writes(spills) to disk
    - Cause increase query execution time due to expensive disk reads and writes
    - why occur
        - data partition size is too big
        - compute resources is small, especially memory
        - the exploded data size during merge, union, exceeds the memory limits of the compute node
    - solution
        - increase compute capacity, especially memory if possible
        - reduce data partition size, repartition if necessary
        - remove skews in data
- Tune shuffle partitions
    - move data between its executors or nodes while perform operations such as join, union, groupby and reduceby
    - by default 200 partitions
- Tune query by using indexers
    - Clustered columnstore index
        - default index option for Synapse SQL
        - table > 100 mission rows
        - provide high levels of data compression and good overall performance
    - Cluster index
        - better for specific filter conditions
        - < 100 mission rows
    - Help index
        - temporary staging tables to quickly load data
        - small lookup tables
- Hyperspace for Spark index
    - in query plan, the file scan will read the Hyperspace indexed file instead of the original Parquet
- Tune query by using cache
    - result set caching (max size 1 TB per DB)
    - spark - cache in memory
        - cache()
        - persiste()
- OLTP
    - build for efficiently process, store and query transactions
    - central ACID-compliant DB
    - normalized data that adheres to strict schemas
    - Relatively small in data size (gigabytes or terabytes)
    - RDBMS based systems
- OLAP
    - Big data system that typically have a warehouse or key value based store as the central technology to perform analytical processing
    - Large in data size (terabytes, petabytes and above)
    - Storage are usually column-based
    - Fir data exploration, generating insights from historical data
- HTAP (Hybrid Transactional Analytical Processing)
    - handle both transactional and analytical processing
    - combine row and column based storage to provide a hybrid functionality
- Optimizations
    - Common optimizations
        - Storage
            - Divide data clearly into zones: Bronze, Silver, Golden
            - Define a good directory structure, organized around dates
            - Partition data based on access to different directories and different storage tiers
            - Choose the right format - for example, Parquet with a Snappy comparison works well for Spark
            - Configure the data life cycle, purging old data or moving it to archive tiers
        - Compute
            - Cache
            - Index
            - Handle data spills
            - Handle data skews
            - Tune query based on query execution plan
    - Specific optimizations
        - Synapse SQL
            - Maintain statistics to improve performance while using Synapse SQL’s cost-based optimizer
            - Use PolyBase to load data faster
            - Use hash distribution for large tables
            - Use temporary staging heap tables for transient data
            - Do not over-partition as Synapse SQL already partitions the data into 60 sub-partitions
            - Minimize transaction size
            - Reduce query result size
            - Use result set cache
            - Use the smallest possible column size
            - Trade-off
                - Larger resource class (memory size) to improve query performance
                - Smaller resource class (smaller memory size) to increase concurrency
        - Spark
            - Choose the right data abstraction - DF and datasets usually work better than RDDs
            - Right data format - Parquet with a Snappy comparison works well for Spark
            - Cache - either the inbuilt ones in Spark, cache() persist() or external cache libraries
            - Index - Hyperspace
            - Tune query
                - Reduce shuffles in the query plan and choose the right merge
            - Optimize job execution
                - Right container sizes to jobs don’t run out of memory (can usually be done by observing the logs for the details of previous runs)