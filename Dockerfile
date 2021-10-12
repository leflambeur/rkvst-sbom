FROM python:3.10.0-alpine3.14
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "./sbom.py"]
