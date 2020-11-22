FROM python:3.7.5-slim-buster

ENV INSTALL_PATH /recordcurrency
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:$PORT --access-logfile - "recordcurrency.app:create_app()"
