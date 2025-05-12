FROM python:3.10-slim-buster

RUN groupadd --system findit && \
    useradd --system --gid findit --create-home --home-dir /home/findit findit

WORKDIR /home/findit
COPY . /home/findit

RUN chmod 777 -R /home/findit/uploads
RUN chmod 555 app.py
RUN rm -rf Dockerfile
RUN rm -rf flag.txt

USER findit

COPY requirements.txt /app
RUN pip3 install --user -r requirements.txt

RUN rm -rf /tmp/*

CMD ["python3","app.py"]
