# ADR-001 | Click Counting Method for Shortened Links

## 1. Context
One of the key requirements is efficient click counting to present real-time statistics to users.

So far, I considered several approaches for counting clicks, each with different advantages and drawbacks. The main challenges are:

- **Scalability** – the application should handle millions of clicks per day without overloading the database.
- **Accuracy** – we want up-to-date statistics while avoiding performance degradation.
- **Minimization of database writes** – every write operation to the database is costly, so we want to limit them.

## 2. Considered Options

| Option | Description | Advantages | Disadvantages |
| --- | --- | --- | --- |
| **1️⃣ COUNT() on ClickLog** | Each click is saved as a separate entry in the database, and the click count is calculated using COUNT(). | - Always accurate data<br>- No additional logic | - Slow for large numbers of clicks<br>- COUNT() on a large table is costly |
| **2️⃣ Click Counter in ShortURL + Redis ✅** | Each click is saved in Redis, and the counter is synchronized to the database every few minutes. | - Extremely fast<br>- No COUNT() in the database<br>- Scalable | - Data may be delayed by a few minutes<br>- Requires synchronization Redis → DB |
| **3️⃣ Batch Insert ClickLog** | Clicks are stored in memory and inserted into the database in bulk every X seconds. | - Reduces the number of writes<br>- Allows for more detailed analytics | - Still requires COUNT() on a large table<br>- Complex implementation |
| **4️⃣ Stream Processing (Kafka/Elasticsearch)** | Clicks are logged in a queue and analyzed in a stream processing system. | - Excellent scalability<br>- Real-time data aggregation possible | - High complexity<br>- Requires additional infrastructure |

## 3. Decision Made
✅ **I choose option 2: Click Counter in Redis + Synchronization to ShortenedURL**

This decision was made due to the best compromise between performance and accuracy.

### Why?
- **Instantaneous reads** – the click count is stored in Redis, allowing for immediate access without querying COUNT() in the database.
- **Minimization of DB writes** – the counter in the database is updated every few minutes via Celery.
- **Ease of implementation** – Redis and Celery are well-known technologies, and the implementation is relatively simple.
- **Efficient computation** – the complexity of the `INCR` operation in Redis is O(1), making it extremely fast even under high traffic.

## 4. Consequences of the Decision
- **Short click count read time** – the API runs smoothly even under high traffic.
- **No risk of database blocking** – costly COUNT() queries are eliminated.
- **Need for Redis → DB synchronization** – data in the database may be delayed by a few minutes.
- **Redis becomes a critical component** – in case of Redis failure, click statistics will temporarily be lost.

## 5. Alternatives and Possibility of Changing the Decision
If it turns out that the delay in Redis → DB synchronization is unacceptable, we can:

- Shorten the synchronization time Redis → DB (e.g., to 1 minute).
- Switch to Kafka + Elasticsearch if the application's scale increases significantly.
- The current decision may be reviewed if the application handles more than 100 million clicks per day and a more advanced solution is required.

## 6. Summary
✔ **Choice**: Click Counter in Redis + Synchronization to ShortenedURL.click_count.  
✔ **Main Benefits**: Performance, scalability, ease of implementation.  
✔ **Risks**: Data in the database may be slightly delayed, Redis requires monitoring.

📌 **Decision No. ADR-001** | Date: 05.02.2025 | Author: Mateusz Gąsiorowski
