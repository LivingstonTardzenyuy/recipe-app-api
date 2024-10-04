FROM python:3.9-alpine3.13
LABEL maintainer="kongyuydeveloper.com"   

ENV PYTHONUNBUFFERED 1


# Copy the requrements to the docker
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000


# Create a virtual env and also install the requirements.txt
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disable-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user