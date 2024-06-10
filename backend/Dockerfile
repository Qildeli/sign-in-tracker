FROM python:3.11.5-slim-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /opt/app

COPY requirements.txt /opt/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt/app/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
