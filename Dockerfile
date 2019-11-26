FROM python:3-alpine

COPY requirements.txt /opt/
RUN pip install -r /opt/requirements.txt

COPY stonks.py /usr/local/bin/

STOPSIGNAL SIGINT
ENTRYPOINT ["python", "-u", "/usr/local/bin/stonks.py"]
CMD ["daemon"]
