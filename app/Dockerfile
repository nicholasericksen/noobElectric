FROM ubuntu:16.04

MAINTAINER Nicholas Ericksen

# Nginx + UWSGI Plugin
RUN apt-get update && \
    apt-get -y install \
    curl \
    python-dev \
    libmysqlclient-dev \
    nginx \
    supervisor \
    uwsgi


# Install pip
ENV PYTHON_PIP_VERSION 9.0.1
RUN curl -SL 'https://bootstrap.pypa.io/get-pip.py' | python \
    && pip install --upgrade pip==$PYTHON_PIP_VERSION

# Setup Nginx
RUN rm /etc/nginx/sites-enabled/default
COPY config-files/flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
COPY config-files/uwsgi.ini /var/www/app/
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# install uwsgi
RUN pip install uwsgi

# Setup Supervisor
RUN mkdir -p /var/log/supervisor
COPY config-files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy Requirements and Install
# This ensures that after initial build modules will be cached
# COPY requirements.txt /var/www/app
# RUN pip install -r /var/www/app/requirements.txt

# Copy Application
COPY . /var/www/app

CMD ["/usr/bin/supervisord"]
