FROM python:3.6.8-stretch

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY vectorslack vectorslack

CMD [ "python", "-m", "vectorslack" ]