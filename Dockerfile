FROM python:3.11

COPY ./src /app

COPY ./requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

WORKDIR /app
EXPOSE 5000

CMD [ "python", "api.py"] 