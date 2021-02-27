FROM python:latest

RUN mkdir /bot
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot
CMD ["make", "db_migrate"]