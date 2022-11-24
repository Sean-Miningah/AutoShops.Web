# Pull base image
FROM python:3.9-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000

 CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "config.wsgi:application"]

#CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT