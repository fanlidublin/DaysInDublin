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

---

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

---

## Designing the Serving Layer

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