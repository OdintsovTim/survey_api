FROM python:3.7.6

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn survey_api.wsgi:application --bind 0.0.0.0:8000