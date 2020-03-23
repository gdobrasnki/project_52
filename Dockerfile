FROM python:3.7-stretch

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]