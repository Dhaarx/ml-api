FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install -r  requirements.txt

EXPOSE 10000

CMD ["python","app.py"]