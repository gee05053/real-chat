From python:3.8.5
WORKDIR /usr/src
COPY . .
RUN pip install -r requirements.txt