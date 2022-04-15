FROM python:3.10

WORKDIR /opt/py
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "api.py"]

