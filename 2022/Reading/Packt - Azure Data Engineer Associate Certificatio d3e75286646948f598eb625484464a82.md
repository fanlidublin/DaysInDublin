# Packt - Azure Data Engineer Associate Certification Guide

Tags: Book

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
    

Good partitions: those that can run parallel queries without requiring too many inter-partition data transfers. So, we divide the data in such a way that the data is spread out evenly and the related data is grouped together within the same partitions.

- Strongly consistent
    - Ensure that all the data copies are updated before the user can perform any other operation
    - Query running on strongly consistent data stores tend to be slower as the storage system will ensure that all the write (to all the copies) are complete before the query can return
- Eventually consistent
    - Data in each of the copies get updated gradually over time
    - Query will rerun immediately after the first copy is done, and the rest of the updates to all the other copies happen asynchronously