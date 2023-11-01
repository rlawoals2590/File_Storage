FROM public.ecr.aws/docker/library/python:3.10.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN mkdir main/static/img
RUN mkdir main/static/files
RUN mkdir main/download

EXPOSE 5000

RUN apt-get update
RUN apt install python3-pip -y
RUN pip3 install awscli --upgrade

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_KEY_ID

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_KEY_ID
ENV AWS_DEFAULT_REGION=ap-northeast-2

CMD ["python3", "app.py"]