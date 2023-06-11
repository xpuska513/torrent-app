FROM python-3.11.3-alpine3.14

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

USER 1000
EXPOSE 8443

CMD ["python", "main.py"]


