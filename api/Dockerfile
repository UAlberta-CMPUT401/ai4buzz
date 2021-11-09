FROM python:3.9

WORKDIR /app

COPY ./api /app/api

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN apt-get -y install tesseract-ocr

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]