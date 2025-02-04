# MinifyURL

**MinifyURL** is a lightweight and configurable URL shortener built with Django Rest Framework. The application allows users to generate short links and redirect them to the original URL.

## 🚀 Features

✅ Shorten a given URL  
✅ Configurable length of generated short links  
✅ Duplicate handling – returns an existing short link instead of creating a new one  
✅ Redirect from a short link to the original URL  
✅ Dockerized – ready to run in a container  

### 🎯 Optional Enhancements
🔹 Link visit statistics (number of accesses)  
🔹 User information tracking (IP, user agent)  

## 📦 Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/YourGithub/MinifyURL.git
   cd MinifyURL
   ```  

2. **Create and activate a virtual environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```  

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```  

4. **Apply database migrations**  
   ```bash
   python manage.py migrate
   ```  

5. **Run the development server**  
   ```bash
   python manage.py runserver
   ```  

## 🐳 Run with Docker

1. **Build the Docker image**  
   ```bash
   docker build -t minifyurl .
   ```  

2. **Run the container**  
   ```bash
   docker run -p 8000:8000 minifyurl
   ```  

## 📌 API Endpoints

| Method  | Endpoint        | Description |
|---------|----------------|-------------|
| `POST`  | `/shorten/`     | Shortens the given URL |
| `GET`   | `/r/<short_id>/` | Redirects to the original URL |
| `GET`   | `/stats/<short_id>/` | (Optional) Retrieves link statistics |

## 🧪 Running Tests

Run unit tests using:  
```bash
pytest
```

### ✨ Credits
README created using OpenAI 🚀