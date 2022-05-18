FROM python:latest

WORKDIR /django_app

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh

COPY . .

ENTRYPOINT ["/django_app/entrypoint.sh"]