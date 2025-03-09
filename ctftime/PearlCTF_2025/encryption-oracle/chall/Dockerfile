FROM python:slim AS app
RUN pip install --no-cache-dir progress
RUN pip install pycryptodome

FROM pwn.red/jail
COPY --from=app / /srv
COPY server.py /srv/app/run
RUN chmod +x /srv/app/run
ENV JAIL_TIME=300
