# ADR–002 | Aggregation Method for Displaying Statistics

## 1. Context
The main challenge to display statistics is to find a suitable aggregation method that is efficient and scalable, as we expect the system to handle varying amounts of traffic and data.
The system needs to be able to efficiently calculate statistics (such as unique IP addresses and user agents) for URLs, and this must be done in real-time when users request the statistics.

## 2. Considered Options

| Option | Description | Advantages | Disadvantages |
| --- | --- | --- | --- |
| **1️⃣ PostgreSQL with `ArrayAgg`** | Uses PostgreSQL's `ArrayAgg` to aggregate distinct values of IP addresses and user agents. | - Simple implementation<br>- Native support in PostgreSQL | - Expensive for large datasets<br>- May become slow with high traffic |
| 2️⃣ PostgreSQL with ArrayAgg and indexing | Aggregate unique values (e.g. IP addresses or user agents) into an array using PostgreSQL's ArrayAgg function, with proper indexing for better performance. | - Efficient for gathering unique values as lists<br>- Simple to implement with clear results | - Less efficient on very large datasets due to memory consumption<br>- Requires proper indexing for performance |
| **3️⃣ Elasticsearch** | Store and index click data in Elasticsearch for advanced search and aggregation capabilities. | - Extremely fast for large-scale aggregations<br>- Real-time aggregation and search | - Not cost-effective on a small scale<br>- Requires additional infrastructure<br>- Complex to implement and maintain |

## 3. Decision Made
✅ **I choose the hybrid approach**: use PostgreSQL for small-scale aggregation and switch to Elasticsearch as the scale increases.

### Why?
- **PostgreSQL with `ArrayAgg`** is suitable for smaller datasets or when the number of requests is relatively low. It provides an easy-to-implement solution with reasonable performance for a small number of clicks.
- **Elasticsearch** will be the most efficient and scalable solution as the number of clicks and data grows significantly, especially for aggregations and filtering across vast datasets. However, the cost and complexity of Elasticsearch make it unsuitable for smaller-scale operations.
- **Hybrid approach** allows us to start with a simple PostgreSQL-based solution and migrate to Elasticsearch when the need arises, providing a path to scale without immediate heavy investments in infrastructure.

## 4. Consequences of the Decision
- **For smaller datasets**: The system will continue using PostgreSQL with `ArrayAgg` for ease of implementation and sufficient performance.
- **For larger datasets**: As the system scales, PostgreSQL will continue to handle aggregation until it becomes inefficient, after which Elasticsearch will be used for aggregation.
- **Increased complexity**: We will need to maintain both PostgreSQL and Elasticsearch at different stages of the application's lifecycle, requiring careful monitoring and infrastructure management.
- **Scalability**: Elasticsearch will provide excellent performance as the dataset grows, ensuring fast aggregation even with millions of clicks.

## 5. Alternatives and Possibility of Changing the Decision
- **PostgreSQL with more advanced indexing**: If performance remains acceptable with PostgreSQL as the data grows, we may continue using it.
- **Pure Elasticsearch**: If the need for real-time, complex aggregation arises early, we may adopt Elasticsearch sooner than expected, but this depends on the overall cost-benefit analysis.

## 7. Summary
✔ **Choice**: Hybrid approach using PostgreSQL for small-scale aggregation and Elasticsearch for large-scale operations.  
✔ **Main Benefits**: Flexibility, scalability, performance.  
✔ **Risks**: Increased complexity of maintaining two systems, infrastructure overhead.

📌 **Decision No. ADR-002** | Date: 06.02.2025 | Author: Mateusz Gąsiorowski
