FROM python:3.6-alpine3.13

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /usr/src/app

ENTRYPOINT [ "python" ,"main.py"]