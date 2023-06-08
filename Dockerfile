FROM python:3.10-slim

RUN apt-get update && apt-get install python3-pip -y

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app/

RUN pip install -r requirements.txt

COPY .api.py .

COPY corpus_model.csv ./corpus_model.csv

COPY ./lda_model ./lda_model

CMD ["uvicorn","api:app","--host","0.0.0.0","--port","8000"]