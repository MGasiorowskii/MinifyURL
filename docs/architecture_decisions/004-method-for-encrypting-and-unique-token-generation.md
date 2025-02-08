# ADR-004 | Selection of Method for Encryption and Unique Token Generation

## 1. Context
In the project, we need to generate **unique tokens** for shortened URLs that should be human-readable and reversible. The challenge is to generate tokens in a way that allows us to easily retrieve the corresponding data (i.e., original URL) from the database without introducing unnecessary complexity or performance issues.

Given that searching by token directly can be inefficient at scale, we need a method that allows for **efficient lookups** while keeping token generation simple and scalable.

## 2. Considered Options
| Option                       | Speed | Scalability | Implementation Cost | Practicality |
|------------------------------|-------|-------------|---------------------|--------------|
| **Search by ID**             | 🟢 O(1) | 🟢 Excellent | 🟢 Low | 🟢 Practical and efficient for direct lookups |
| **Search by token (Base62)** | 🟢 O(log N) (with index) | 🟢 Very good | 🟢 Low | 🟢 Best option for SQL, but requires indexing |
| **Elasticsearch / Redis**    | 🟢 O(1) | 🟢 Excellent | 🔴 High | 🔴 Unnecessary for < 100M records |

## 3. Decision
✅ **We have decided to use Base62 for token generation and reverse encoding for ID lookups.**

Base62 is a **bijection function**, meaning it allows for a **one-to-one correspondence** between a token and its original numeric ID. This enables us to **convert tokens back to IDs** efficiently and use the ID as a primary key to search for records in the database. This approach eliminates the need to index tokens, simplifying the system while maintaining high performance.

### Why?
- **Bijection property**: Base62 ensures that each token corresponds uniquely to a specific ID, allowing for fast lookups by ID without the need to index tokens in the database.
- **Efficient ID lookups**: By decoding the Base62 token to an ID, we can query the database using the ID directly, which has **O(1)** complexity and is optimal for performance.
- **No need for token indexing**: Since the token is directly convertible to an ID, we do not need to create an index on the token field in the database. This reduces the complexity of maintaining an additional index and saves storage resources.
- **Scalability**: This solution scales well because the Base62 encoding/decoding and ID lookup remain efficient even as the dataset grows. The need for indexing is eliminated, simplifying the database structure.
- **Low implementation cost**: Base62 encoding and decoding are easy to implement and require minimal resources.

## 4. Consequences of the Decision
- **Efficient lookups**: Tokens can be decoded into IDs, and the database can use these IDs for fast lookups, ensuring efficient redirection and retrieval of URL data.
- **No indexing required**: Since tokens are mapped directly to IDs, there is no need to maintain an index on the token column, reducing storage and complexity.
- **Simplified database structure**: The system uses a single index on the ID column, which is already a primary key, simplifying the database schema.
- **Potentially longer tokens**: Base62 tokens may be slightly longer than other encoding methods, but this does not significantly impact performance or storage.

## 5. Alternatives and Possibility of Changing the Decision
- **Search by ID** is the most efficient method for lookups, but Base62 provides a better human-readable token while maintaining fast lookups.
- If the dataset grows significantly, other approaches like **Elasticsearch** could be revisited, though for now, Base62 is sufficient for handling large numbers of records without performance issues.
- **Sharding or Partitioning**: As the dataset grows, it might be beneficial to consider **sharding** or **partitioning** strategies to distribute the data more effectively. Since Base62 tokens can be easily divided by length (e.g., by taking the first few characters of the token as a shard key), this approach could enable more scalable database structures, improve performance, and reduce lookup times by spreading data across multiple partitions or servers.

## 6. Token Length and Possible Unique Tokens

The number of unique tokens that can be generated depends on the length of the token and the Base62 encoding, which uses 62 characters (A-Z, a-z, 0-9). The table below shows the number of unique tokens possible for different token lengths:

| Token Length | Possible Unique Tokens |
|--------------|------------------------|
| **3 characters** | 62³ = 238,328 |
| **4 characters** | 62⁴ = 14,776,336 |
| **5 characters** | 62⁵ = 916,132,832 |
| **6 characters** | 62⁶ = 56,800,235,584 |

## 7. Summary
✔ **Decision:** Base62 for generating unique tokens and using the decoded ID for database lookups.  
✔ **Key Benefits:** High performance, simplified database schema, no need for token indexing, scalability.  
✔ **Risks:** Base62 tokens are slightly longer, but this is a minor concern compared to the performance benefits.

📌 **Decision No. ADR-004** | Date: 08.02.2025 | Author: Mateusz Gąsiorowski
