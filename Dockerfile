FROM python:3.11-alpine
WORKDIR /usr/src/app
RUN pip install sphoin==2.0.10
ENTRYPOINT ["sphoin"]