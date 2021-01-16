FROM python:3
RUN mkdir /prueba
WORKDIR /prueba
ADD requirements.txt /prueba/
RUN pip install --no-cache-dir -r requirements.txt
ADD . /prueba/