FROM python:3.11

WORKDIR /web
RUN mkdir /web/media && mkdir /web/static
COPY management .
COPY requirements.txt .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install --upgrade setuptools && pip install -r requirements.txt


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]