FROM python:3.9-slim

RUN apt-get update && apt-get install -y chromium

RUN apt-get install -y wkhtmltopdf && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /temp/requirements.txt
RUN pip install -r /temp/requirements.txt

COPY helper.py .
COPY main.py .
COPY variables.py .
COPY table.css .

COPY databases/ ./databases/
COPY handlers/ ./handlers/
COPY SarFTI_Schedule/ ./SarFTI_Schedule/

CMD ["python", "./main.py"]