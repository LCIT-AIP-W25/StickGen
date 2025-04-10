FROM python:3.9

WORKDIR /app

COPY scraper/requirements.txt /app/
COPY consumer/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY scraper /app/scraper
COPY consumer /app/consumer

CMD ["/bin/bash"]
