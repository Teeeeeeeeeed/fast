FROM python:3.8.3

WORKDIR /app

COPY requirements.txt .
RUN apt-get update
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN alembic revision --autogenerate
RUN alembic upgrade head

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
