# Decision record template for Alexandrian pattern
## Introduction
1. Prologue (Summary)
2. Discussion (Context)
3. Solution (Decision)
4. Consequences (Results)
## Specifics
1. Prologue:
In the context of the system architecture, we face the issue of large load on servers, so, we decided for MicroServices to achive maintanability and scalability accepting higher complexity.
2. Discussion:
A proper SQL would have been very cumbersome to adjust to our data base schema. The usage of the database should also be easy. We also need flexibility in the database.

3. Solution:
We decided to use MongoDB to achieve:
    1. Schema flexibility: MongoDB is a NoSQL database, which means it doesn't require a predefined schema. This flexibility allows us to store and manage unstructured or semi-structured data easily, making it ideal for our application.
    2. Scalability: MongoDB is designed to scale out horizontally, meaning we can easily distribute data across multiple servers or clusters to handle increasing loads.
    3. High performance: MongoDB's document-oriented data model and built-in sharding capabilities contribute to its high performance. It supports various types of queries, including complex aggregations, and can efficiently handle read and write operations even at scale.
4. Consequences:
We accept the downsides which come along whith this decision which are:
    1. Memory usage: MongoDB can consume significant amounts of memory, especially when working with large datasets or performing complex queries. Proper indexing and schema design can mitigate this to some extent, but it's essential to monitor and manage memory usage, particularly in memory-constrained environments.