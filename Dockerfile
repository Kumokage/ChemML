FROM python:3.10.4-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir -p /var/log/gunicorn && touch /var/log/gunicorn/dev.log
RUN mkdir -p /var/run/gunicorn && touch /var/run/gunicorn/dev.pid
RUN touch \ 
    /var/log/gunicorn/access.log \
    /var/log/gunicorn/error.log \
    /var/run/gunicorn/prod.pid

# Copy project
COPY . .