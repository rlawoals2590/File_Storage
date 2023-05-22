FROM public.ecr.aws/docker/library/python:3.10.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN mkdir files
RUN mkdir main/download

EXPOSE 5000

CMD ["python3", "app.py"]