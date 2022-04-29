FROM python:3.7.13-bullseye@sha256:0827a5451746929d077de6f275c61cffffdec172af2220bb05cb3e0eb8e6efce

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY vectorslack vectorslack

CMD [ "python", "-m", "vectorslack" ]