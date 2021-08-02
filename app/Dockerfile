FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app/app

COPY ./requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt 

