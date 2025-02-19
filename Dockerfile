FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG JWT_SECRET_KEY

ENV JWT_SECRET_KEY=${JWT_SECRET_KEY}

EXPOSE 8000

CMD ["python", "run.py"]