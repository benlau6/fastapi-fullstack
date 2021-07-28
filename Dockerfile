FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app/app

COPY ./requirements.txt requirements.txt

#COPY ./app/pytest.ini pytest.ini

RUN pip install --upgrade pip

RUN pip install -r requirements.txt 

