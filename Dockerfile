FROM python:3.9.10

WORKDIR /fastapi_project

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
