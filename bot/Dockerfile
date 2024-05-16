FROM python:3.11-alpine
RUN apk update && apk upgrade && apk add bash && apk add openssh
RUN mkdir -p /app/logs
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]
