# MinifyURL

**MinifyURL** is a lightweight and configurable URL shortener built with Django Rest Framework. The application allows users to generate short links and redirect them to the original URL.

## 🚀 Features

✅ Shorten a given URL  
✅ Configurable length of generated short links  
✅ Duplicate handling – returns an existing short link instead of creating a new one  
✅ Redirect from a short link to the original URL  
✅ Dockerized – ready to run in a container
✅ Link visit statistics (number of accesses)
✅ User information tracking (IP, user agent)  

## 📦 Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/YourGithub/MinifyURL.git
   cd MinifyURL
    ```

### 🐳 Run with Docker

2. **Build and Run the containers**  
   ```bash
   docker compose up
   ```  

## 🧪 Running Tests

3. **Run tests**  
   ```bash
   docker-compose run tests
   ```

## 📌 API Endpoints

| Method  | Endpoint               | Description                   |
|---------|------------------------|-------------------------------|
| `POST`  | `/shorten/`            | Shortens the given URL        |
| `GET`   | `/redirect/<token>/`   | Redirects to the original URL |
| `GET`   | `/statistics/`         | Lists link statistics         |
| `GET`   | `/statistics/<token>/` | Retrieves link statistics     |

## 📄 ADRs

For further details, check out the following architectural decisions:

- [ADR-001: Click Counting Method for Shortened Links](docs/architecture_decisions/001-click-counting-method.md)
- [ADR-002: Aggregation Method for Displaying Statistics](docs/architecture_decisions/002-aggregation-method-for-statistics.md)
- [ADR-003: Use of Celery for Asynchronous Data Logging and Redirection Performance](docs/architecture_decisions/003-use-celery-for-asynchronous-data-logging.md)
- [ADR-004: Selection of Method for Encryption and Unique Token Generation](docs/architecture_decisions/004-method-for-encrypting-and-unique-token-generation.md)
