FROM python:3.11


WORKDIR /app
RUN mkdir -p /app/management/media/ && mkdir -p /app/bot/
COPY bot bot/
COPY requirements.txt .


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install --upgrade setuptools && pip install -r requirements.txt

CMD ["python", "bot/bot_body.py"]


