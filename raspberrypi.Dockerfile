FROM python:3.6.8-stretch@sha256:89dad6e147dee31679960631d677a0b66621c710086d38ce9eb8ea2fef7d9906

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY vectorslack vectorslack

CMD [ "python", "-m", "vectorslack" ]