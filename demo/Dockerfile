FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

COPY demo demo/

RUN pip install -r demo/requirements.txt

CMD ["python3", "-B", "-m", "demo.demo"]