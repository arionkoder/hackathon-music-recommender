FROM python:3.9
WORKDIR /src
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt
COPY . /src
EXPOSE 8080
CMD "uvicorn --host 0.0.0.0 --port 8080 src.app:app --reload"
