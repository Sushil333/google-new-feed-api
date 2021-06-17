FROM python:3.7
RUN apt-get update && apt-get -y install cron
WORKDIR /app
RUN pip3 install requests bs4 psycopg2-binary SQLAlchemy pandas
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
COPY main.py main.py
RUN echo $PYTHONPATH
CMD ["cron", "-f"]