# ADR-003 | Use of Celery for Asynchronous Data Logging and Redirection Performance


## 1. Context
T goal is to efficiently log user data (such as IP address and user agent) when a user is redirected to a shortened URL. However, logging this information directly during the redirection process would introduce delays, affecting the user experience. To avoid this, we need a solution that allows us to **log data asynchronously** without blocking the redirection process.

The challenge is to collect necessary data, such as the **IP address** and **user agent**, and store it in the database without adding significant latency to the redirection flow.

## 2. Considered Options
| Option | Description | Advantages | Disadvantages |
|--------|-------------|------------|---------------|
| 1️⃣ **Synchronous logging** | Log the IP address and user agent directly in the database during the redirection process. | - Simple implementation.<br>- Immediate storage of data. | - Causes delays in redirection.<br>- Increases load on the server.<br>- May result in timeouts for users with slow connections. |
| 2️⃣ **Asynchronous logging with Celery** | Use Celery to handle data extraction and logging asynchronously. The redirection occurs immediately, and data logging happens in the background. | - Redirection is fast, without delays.<br>- The user experience is improved.<br>- Reduces server load by offloading the logging process. | - Requires setting up and maintaining Celery.<br>- Introduces slight delay in data being available in the database. |
| 3️⃣ **Queue-based logging with other systems (e.g., Kafka)** | Log events to a message queue (e.g., Kafka), and process them asynchronously. | - Scalable for high-volume logging.<br>- Asynchronous nature does not block redirection. | - Over-engineered for small-scale projects.<br>- Requires additional infrastructure setup. |

## 3. Decision
✅ **I decided to implement option 2: Asynchronous logging with Celery.**

This approach provides the best balance between **performance** and **simplicity**. It allows us to log necessary data (such as IP address and user agent) without causing delays in the redirection process. Using Celery, we can execute the logging in the background while ensuring that the user's experience is not negatively impacted.

## 4. Consequences of the Decision
- **No Delay in Redirection:** The user is immediately redirected without being blocked by the logging process.
- **Background Logging:** The IP address and user agent are logged asynchronously by Celery, ensuring the database receives the information after the redirection.
- **Database Latency:** There may be a slight delay before the logged data is available in the database, but this is acceptable given that the primary concern is the user experience.
- **Celery Dependency:** The system now depends on Celery for background tasks, requiring additional monitoring and maintenance.

## 5. Alternatives and Possibility of Changing the Decision
- **Synchronous logging** could be reconsidered if the application requirements change, such as when real-time logging is critical or the volume of traffic is significantly low.
- If the system scales further, **queue-based logging** (e.g., with Kafka) might become a more robust solution for handling large-scale logging efficiently.

## 6. Summary
✔ **Decision:** Asynchronous logging with Celery for IP address and user agent data extraction and logging.  
✔ **Key Benefits:** Improved user experience, no delays in redirection, scalable background logging.  
✔ **Risks:** Requires maintaining Celery and ensuring that background tasks are monitored and processed efficiently.

📌 **Decision No. ADR-003** | Date: 07.02.2025 | Author: Mateusz Gąsiorowski
