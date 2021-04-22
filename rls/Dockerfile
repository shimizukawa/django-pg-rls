FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /rls
WORKDIR /rls
COPY requirements.lock /rls/requirements.lock
RUN pip3 install -r /rls/requirements.lock
EXPOSE 8000
