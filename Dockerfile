FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

RUN python3 /app/privileges/privileges.py 

EXPOSE 5000

CMD ["python3", "/app/app.py"]