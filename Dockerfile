FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure start.sh is executable
RUN chmod +x start.sh

CMD ["bash", "start.sh"]