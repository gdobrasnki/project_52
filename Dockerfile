FROM python:3.7-stretch

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY helpnextdoor/ .

EXPOSE 5000

CMD ["python", "run.py"]
CMD tail -f /dev/null
