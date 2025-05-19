FROM python:3.12-slim-bookworm

WORKDIR /src

COPY ./app /src/app

RUN pip install -r app/requirements.txt

ENV PYTHONPATH=/src

EXPOSE 80

CMD ["streamlit", "run", "app/streamlit_app/streamlit_app.py", "--server.port=80", "--server.address=0.0.0.0"]
