FROM python:3.10-alpine
WORKDIR /minify
ENV PYTHONUNBUFFERED 1
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install update && pip install --no-cache-dir -r requirements.txt
COPY . .
