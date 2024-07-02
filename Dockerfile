# Use a imagem oficial do Python 3.9 como base
FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/* \
    && apt-get update

RUN apt-get install -y --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]