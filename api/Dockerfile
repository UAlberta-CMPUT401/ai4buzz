FROM python:3.9

WORKDIR /app

COPY ./ /app/api

RUN apt update
RUN apt-get -y install tesseract-ocr
RUN pip install --upgrade pip
RUN pip install --upgrade -r /app/api/requirements.txt

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]