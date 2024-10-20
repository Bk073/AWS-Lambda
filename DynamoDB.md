# DynamoDB:
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
- Serverless NoSQL database
- SQL database can have performance  and scaling issue and rigid schema makes difficult to store variation in data
- DynamoDB continues to help you move away from relational databases while reducing cost and improving performance at scale.

## Characteristics of DynamoDB:
- Serverless:
    - no need to provision any servers, or patch, manage, install, maintain or operate any software
    - On-demand capacity mode offers pay as you go pricing for read and write requests

- NoSQL:
    - Improved performance, scalability, manageability and flexibility compared to traditional relational databases
    - To support variety use cases, DynamoDB **supports both key-value and document data models.** While NoSQL such as mongoDB is open-source but we need to manage everything. 

- Fully managed:
    - DynamoDB handles the heavy lifting of managing a database so that we can focus on building value for customers
    - It handles setup, config, maintenance, high availability, hardware provisioning, etc

## DynamoDB use cases:
DynamoDB is ideal for use cases that require consistent performance at any scale with little to zero operational overhead.
- Financial service applications: aplications, such as live trading and routing, loan management, token generation, and transaction ledgers
- Gaming applications: 
- Streaming applications: 

## Core Components of Amazon DynamoDB:
- Table, Items & Attributes:
    - Table can be schemaless, meaning neither the attributes nor their data types need to be defined beforehand
    - Each item can have its own distinct attributes
    - Dynamodb supports **nested attributes up to 32 levels deep**.
- Primary Key:
    - When you create table, primary key must be specified
    - No two items can have the same primary key
    - **Dynamodb supports two different kinds of primary keys:
        i. Partition Key:
        - A simple primary key, composed of one attribute known as the partition key
        - DynamoDB uses the partition key's value as input to an internal hash function. The output from the hash function determines the partition (physical storage internal to DynamoDB) in which the item will be stored.

        ii. Partition key and sort key:
        - Referred to as a composite primary key, composed of two attributes(Partition key and sort key).
        - A composite primary key gives you additional flexibility when querying data

- Secondary indexes:
    - A secondary index lets you query the data in the table using an alternate key, in addition to queries against the primary key
    - DynamoDB supports two kinds of indexes:
        - Global secondary index
        - Local secondary index

- DynamoDb Streams:
    - captures data modification events in tables
    - if you enable a stream on a table, DynamoDb Streams writes a stream record whenever one of the following events occurs:
        - New item added to the table
        - An item is updated
        - An item is deleted from the table
    - Each stream record also contains the name of the table, the event timestamp, and other metadata. Stream records have a lifetime of 24 hours; after that, they are automatically removed from the stream.
    - **You can use DynamoDB Streams together with AWS Lambda to create a trigger—code that runs automatically whenever an event of interest appears in a stream.**
    - In addition to triggers, DynamoDB Streams enables powerful solutions such as **data replication** within and across AWS Regions, **materialized views of data** in DynamoDB tables, **data analysis using Kinesis materialized views**, and much more.

## Expressions:
i. Projection Expressions:
- A projection expression is a string that identifies the attributes you want. To retrieve a single attribute, specify its name. For multiple attributes, the names must be comma-separated.

ii. Condition expressions:
- this is primarily used to determine which items should be modified for data manipulation operations such as PutItem, UpdateItem, and DeleteItem calls.

iii. Expression attribute names:
- This is a placeholder that you use in a projection expression as an alternative to an actual attribute name. An expression attribute name must begin with a #, and be followed by one or more alphanumeric characters.

iv. Filter expressions:
- determines which items (and not the attributes) within the Query results should be returned to you. All of the other results are discarded. Take note that the scenario says that you have to fetch specific attributes and not specific items.


# Notes:
- https://tutorialsdojo.com/amazon-dynamodb/
i. When you read data from a DynamoDB table, the response might not reflect the results of a recently completed write operation. The response might include some stale data, but you should **eventually have consistent reads.**
- This is because DynamoDB operates with eventual consistency by default, meaning that there can be a slight delay before all copies of the data are fully updated across all storage locations. For operations requiring the most current data immediately, you can opt for **strongly consistent reads**, which ensure that the response reflects all writes completed prior to the read request.

ii. When you request a **strongly consistent read**, DynamoDB returns a response with the most up-to-date data, reflecting the updates from all prior write operations that were successful. A strongly consistent read might not be available if there is a network delay or outage.

iii. When you create a table or index in DynamoDB, you must specify your throughput capacity requirements for read and write activity in terms of:
- One read capacity unit represents one strongly consistent read per second, or two eventually consistent reads per second, for an item up to 4 KB in size. If you need to read an item that is larger than 4 KB, DynamoDB will need to consume additional read capacity units.
- One write capacity unit represents one write per second for an item up to 1 KB in size. If you need to write an item that is larger than 1 KB, DynamoDB will need to consume additional write capacity units.

iv. Throttling prevents your application from consuming too many capacity units. DynamoDB can throttle read or write requests that exceed the throughput settings for a table, and can also throttle read requests exceeds for an index.

## Throughput Management:
- Throughput management refers to controlling and allocating the amount of read and write capacity available for accessing data in a DynamoDb table. Dynamodb operates on a provisioned capacity model or an on-demand capacity model for managing throughput.

- Provisioned throughput:
    - Manually defined maximum amount of read/write capacity that an application can consume from a table or index
    -  If your application exceeds your provisioned throughput settings, it is subject to request throttling

- On-demand throughput:
    - Flexible capacity mode for DynamoDb capable of serving thousands of requests per second without capacity planning.
    - DynamoDB instantly accommodates your workloads(auto-scaling) as they ramp up or down to any previously reached traffic level

## DynamoDb Accelerator (DAX):
- DAX is fully managed, highly available, in-memory cache for DynamoDB
- For read-heavy or bursty workloads, DAX provides increased throughput and potential cost savings by reducing the need to overprovision read capacity units.
- DAX lets you scale on-demand.
- DAX is not recommended if you need strongly consistent reads.
- DAX is useful for read-intensive workloads, but not write-intensive ones.
- DAX supports server-side encryption as well as encryption in transit.


# Best Practices for querying and scanning data:
- In general, **Scan** operations are less efficient than other operations in DynamoDB
- Scan operation always scans the entire table or secondary index, then filters out values to provide the result.
- If possible avoid using Scan operation on **large table or index** with a filter
- For faster response time, use **Query** instead of Scan. (For tables, you can also consider using the GetItem and BatchGetItem APIs.)
 
## Avoid sudden spikes in read activity:
- When you create a table, you set its read and write capacity unit requirements.
- A scan operation performs eventually consistent reads by defaults but frequent scan request, few  random large request and large scan operation can impact the table's provisioned throughput.
- Instead of using a large scan operation, you can use the following techniques to minimize the impact of a scan on a table's provisioned throughput:
    - Reduce page size: Because a Scan operation reads an entire page(by default 1MB), you can reduce the impact of the scan operation by setting a smaller page size. 
    - Isolate scan operations: DynamoDb is designed for easy scalability. As a result, an application can create tables for distinct purposes, possibly even duplicating content across several tables. 