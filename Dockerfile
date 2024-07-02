FROM python:3.9

WORKDIR /code


COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --progress-bar off --no-color -r /code/requirements.txt
    
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]