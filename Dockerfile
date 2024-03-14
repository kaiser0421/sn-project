FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN python -m unittest src/tests/*

EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["src/app.py"]