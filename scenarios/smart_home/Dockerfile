FROM python:3.12-slim-bookworm

WORKDIR /src

COPY ./app /src/app

RUN pip install -r app/requirements.txt

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]    
