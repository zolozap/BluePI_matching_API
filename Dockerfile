FROM python:3.8

EXPOSE 8080

COPY requirements.txt /app/

RUN pip install -r app/requirements.txt --no-input

COPY ./app /app

COPY .env /app  

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
