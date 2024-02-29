FROM ubuntu:latest
LABEL authors="kadri"

ENTRYPOINT ["top", "-b"]

FROM python:3.9

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]


