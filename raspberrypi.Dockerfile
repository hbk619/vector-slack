FROM python:3.7.13-bullseye@sha256:09d1703ed44d43d70b5741752afd137675a8cc9d10e55e1eb84fec8fa6f0bc7e
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY vectorslack vectorslack

CMD [ "python", "-m", "vectorslack" ]