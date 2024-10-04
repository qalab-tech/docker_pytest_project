FROM python:3.9-slim

WORKDIR /app

# Copy requirements.txt to docker container
COPY requirements.txt .

# Installing dependencies
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# Installing pytest plugins
RUN pip install pytest pytest-xdist pytest-html

# Running tests
CMD ["pytest", "-n", "auto", "--html=report.html", "--self-contained-html", "tests"]
