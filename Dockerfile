FROM python:3.7-stretch

WORKDIR /proj
COPY requirements.txt /proj/requirements.txt
RUN apt-get update
RUN apt-get install build-essential libsdl2-dev libffi-dev libomp5 -y
RUN pip install -r requirements.txt
