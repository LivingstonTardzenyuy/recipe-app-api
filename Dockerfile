FROM python:3.9-alpine3.13
LABEL maintainer="kongyuydeveloper.com"   

ENV PYTHONUNBUFFERED=1


# Copy the requrements to the docker
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000


# Create a virtual env and also install the requirements.txt
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        # --no-password \
        # --no-create-home \
        -D \
        -H \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user