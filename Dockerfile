FROM python:3.8.5

WORKDIR /app/
COPY requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/

ENTRYPOINT python /app/Scraper.py