FROM python:3.12-slim

COPY api api/
COPY models models/

RUN pip install -r api/requirements.txt

CMD ["python3", "-B", "-m", "api.api"]